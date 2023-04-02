#coding=utf-8

import logging,subprocess
from multiprocessing import Process,Queue,Event
from paramiko_ssh import myParamiko
class ssh_tool:
    def __init__(self,logger=None,logger_name=None):
        self.logger_name=logger_name
        self.logger=self.get_logger(logger)
    def get_logger(self,logger):
        if not logger:
            logger_name = self.logger_name
            if not logger_name:
                logger_name="tool"
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.INFO)  # 设置logger日志等级
            # 创建handler
            ch = logging.StreamHandler()
            # 设置输出日志格式
            formatter = logging.Formatter(
                fmt="%(name)s-%(levelname)s-%(asctime)s-%(filename)s-%(module)s-%(funcName)s:%(lineno)d %(message)s",
                datefmt="%Y/%m/%d %X"
            )
            # 注意 logging.Formatter的大小写

            # 为handler指定输出格式，注意大小写
            #fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            # 为logger添加的日志处理器
            #logger.addHandler(fh)
            logger.removeHandler(ch)
            logger.addHandler(ch)
            #logger.addFilter(logging.Filter(logger_name))
        return logger

    def exec_command(self,cmds,host_ip,username="root",password=None,port=22):
        if host_ip=="exp_node":
            stdout=subprocess.check_output(cmds,shell=True)
            result=[std.strip().encode("utf-8") for std in stdout.readlines()]
            return result
        print(host_ip,username,password,port,)
        with myParamiko(host_ip,username,password,port,logger=self.logger) as remote:
            self.logger.info("will exec command:%s" % cmds)
            if isinstance(cmds, list):
                result=remote.run_cmdlist(cmds)
            else:
                result=remote.run_cmd(cmds)
            remote.close()
        self.logger.info("on node %s exec command:%s with result:%s" % (host_ip,cmds,result))
        return result
    def send_file(self,host_ip,source_path,target_path,send_case="get",username="root",password="123456",port=22):
        with myParamiko(host_ip,username,password,port,logger=self.logger) as remote:
            if send_case == "get":
                remote.get(source_path,target_path)
            elif send_case == "put":
                remote.put(source_path, target_path)
            else:
                self.logger.info("parameter send_case value %s error,must be 'get' or 'put'" % send_case)
            remote.close()
class mult_process(Process):
    def __init__(self,func,args=(),kwargs={},event=None):
        super(mult_process,self).__init__()
        self.func=func
        self.queue=Queue()
        self.kwargs=kwargs
        self.args = args
        if event != None:
            self.event=Event()
            self.args+=(event,self.event)
    def run(self):
        result=self.func(*self.args,**self.kwargs)
        self.queue.put(result,timeout=3)
    def get_result(self):
        try:
            return self.queue.get(timeout=3)
        except:
            return None


if __name__ == "__main__":
    host_ip="192.168.8.108"
    commds=["ls","pwd"]
    ssh_1_7=ssh_tool()
    print(ssh_1_7.exec_command(commds,host_ip,password="123456"))