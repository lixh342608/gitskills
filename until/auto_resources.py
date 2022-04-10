#coding=utf-8

import os,codecs,yaml,time
from auto_tool.until_funtion.ssh_tool import ssh_tool
from auto_tool.until_funtion.globallogger import globallogger

class resources_auto_install:
    def __init__(self,host_ip,logger=None,password=None,pus_port=9090,pgy_port=9091,exp_port=9100):
        self.logger=self.get_logger(logger)
        self.ssh_handler=ssh_tool(logger=self.logger)
        self.host_ip=host_ip
        self.password=password
        self.platform_type=self.get_system()
        self.pus_port=pus_port
        self.pgy_port=pgy_port
        self.exp_port=exp_port
        self.image_list=["prom/node-exporter","prom/prometheus","grafana/grafana","prom/pushgateway"]
    def get_logger(self,logger):
        if not logger:
            cur_path = os.path.dirname(os.path.realpath(__file__))
            log_file=os.path.join(cur_path,"resources.log")
            logger_handle=globallogger("install_monitor",log_file=log_file)
            logger=logger_handle.log
        return logger
    def get_system(self):
        sys_command="""cat /etc/*-release|grep ^NAME|awk -F "=" '{print $2}'"""
        sys_str=self.ssh_handler.exec_command(sys_command,self.host_ip,password=self.password)
        platform_type=str(sys_str).split()[0].split("\"")[-1].lower()
        return platform_type
    def ins_docker(self,retry_times=3):
        ins_command = "wget -qO- https:\/\/get.docker.com | sh"
        check_command = "docker > /dev/null 2>&1 && echo 0 || echo 1"
        docker_run_comand = "service docker start"
        ret = self.ssh_handler.exec_command(check_command, self.host_ip, password=self.password)
        if int(ret[0]):
            if retry_times <= 0:
                self.logger.info("docker install failed with retry times:3")
                return False
            self.logger.info("Docker install start,Please wait a few minutes.")
            result=self.ssh_handler.exec_command(ins_command,self.host_ip,password=self.password)
            self.logger.info(result)
            ins_ret = self.ins_docker(retry_times - 1)
            return ins_ret
        else:
            self.logger.info("docker install success with ret:%s." % ret)
            result=self.ssh_handler.exec_command(docker_run_comand,self.host_ip,password=self.password)
            self.logger.info(result)
            return True
    def download_img(self):
        will_img=self.check_image()
        if len(will_img) == 0:
            return
        comand_list = []
        for img in will_img:
            cmd="docker pull %s" % img
            comand_list.append(cmd)
        try:
            self.logger.info("download images:{}".format(comand_list))
            result=self.ssh_handler.exec_command(comand_list,self.host_ip,password=self.password)
            self.logger.info(result)
        except:
            pass
        self.download_img()
        return
    def create_conf(self):
        ymls = {
            'global': {
                'scrape_interval': '60s',
                'evaluation_interval': '60s'
            },
            'scrape_configs': [
                {'job_name': 'prometheus',
                 'static_configs': [
                     {
                         'targets': [
                             self.host_ip+":"+str(self.pus_port)
                         ],
                         'labels': {
                             'instance': 'prometheus'
                         },
                     },
                 ]
                 },
                {
                    'job_name': 'linux',
                    'static_configs': [
                        {
                            'targets': [
                                self.host_ip+":"+str(self.exp_port)
                            ],
                            'labels': {
                                'instance': 'localhost'
                            },
                        },
                    ]
                },
                {
                    'job_name': 'pushgateway',
                    'static_configs': [
                        {
                            'targets': [
                                self.host_ip+":"+str(self.pgy_port)
                            ],
                            'labels': {
                                'instance': 'pushgateway'
                            },
                        },
                    ]
                },
            ]
        }
        conf_dir=os.path.dirname(os.path.realpath(__file__))
        conf_path=os.path.join(conf_dir,"prometheus.yml")
        with codecs.open(conf_path,"w") as pf:
            yaml.dump(ymls,pf)
            pf.close()
        time.sleep(1)
        target_dir="/opt/prometheus/"
        target_path=os.path.join(target_dir,"prometheus.yml")
        mkdir_cmd="mkdir -p %s" % target_dir
        result=self.ssh_handler.exec_command(mkdir_cmd,self.host_ip,password=self.password)
        result = self.ssh_handler.send_file(self.host_ip,conf_path,target_path,send_case="put")
        os.remove(conf_path)

    def check_image(self):
        get_image_cmd="docker images|sed '1d'|awk '{print $1}'"
        have_image=self.ssh_handler.exec_command(get_image_cmd,self.host_ip,password=self.password)
        will_imgs=self.image_list.copy()
        self.logger.warning("have images:{}".format(have_image))
        for h in have_image:
            for i in self.image_list:
                if i in h.decode():
                    will_imgs.remove(i)
        self.logger.warning("will images:{}".format(will_imgs))
        return will_imgs
    def run_server(self):
        # 拉起node-exporter容器
        run_nodeexp_command="""docker run -d -p 9100:9100   -v "/proc:/host/proc:ro"   -v "/sys:/host/sys:ro"   -v "/:/rootfs:ro"   --net="host"   prom/node-exporter"""
        # 拉起pushgateway容器
        run_pushgateway_command="docker run -d   --name=pg   -p 9091:9091   prom/pushgateway"
        # 拉起grafanap容器
        run_grafana_command="""docker run -d -p 3000:3000 --name=grafana -v /opt/grafana-storage:/var/lib/grafana grafana/grafana"""
        # 拉起prometheus容器
        run_prometheus_command="""docker run  -d   -p 9090:9090   -v /opt/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml    prom/prometheus"""
        command_list=[run_nodeexp_command,run_pushgateway_command,run_grafana_command,run_prometheus_command]
        try:
            self.ssh_handler.exec_command(command_list, self.host_ip, password=self.password)
        except Exception as e:
            self.logger.warning("run docker service error with msg:%s" % e)
        self.logger.warning("run docker service exec end")
        return
    def set_startboot(self):
        # 设置docker服务开机启动命令
        docker_start_command="systemctl enable docker"
        # 增加/etc/rc.d/rc.local执行权限
        chmod_config_command="chmod +x /etc/rc.d/rc.local"
        # 定义写入初始化文件内容
        start_cmd_str="docker ps -a|sed '1d'|awk '{print \$1}'|xargs docker restart"
        # 删除原有命令，避免文件中存在多个相同任务
        del_docker_start_command="""sed -i "/{0}/d" /etc/rc.d/rc.local""".format(start_cmd_str)
        # 写入开机重拉已有docker命令
        write_docker_restart_command="""echo "{0}" >> /etc/rc.d/rc.local""".format(start_cmd_str)
        command_list=[docker_start_command,chmod_config_command,del_docker_start_command,write_docker_restart_command]
        try:
            self.ssh_handler.exec_command(command_list, self.host_ip, password=self.password)
        except Exception as e:
            self.logger.warning("set start config error with msg:%s" % e)
        self.logger.warning("set start config exec end")
        return
if __name__ == "__main__":
    host_ip="192.168.145.129"
    install_handler=resources_auto_install(host_ip,password="123456")
    if install_handler.ins_docker():
        install_handler.set_startboot()
        install_handler.download_img()
    install_handler.create_conf()
    install_handler.run_server()

