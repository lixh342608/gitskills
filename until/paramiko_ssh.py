#encoding:utf8
#author: djoker
import paramiko,logging,os,time

class myParamiko:
    obj=paramiko.SSHClient()
    obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    def __init__(self,hostip,username="root",password="123456",port=22,logger=None,timeout=300):
        #self.password = self.get_password(password)
        self.logger= logger if logger else logging
        self.timeout=timeout
        pass_list=self.get_password(password)
        try:
            self.obj.connect(hostip,port,username,password=pass_list[0],pkey=pass_list[1])
            self.objsftp = self.obj.open_sftp()
        except Exception as e:
            self.logger.error("Get an exception,type:%s,errormsg:%s" % (type(e),e))
            self.obj.close()
    def get_password(self,password):
        if password:
            pass_list=[password,None]
        else:
            pkey = u"/root/.ssh/id_rsa"
            if not os.path.isfile(pkey):
                pkey=u"C:/Users/Administrator/.ssh/id_rsa"
            pass_list=[None,paramiko.RSAKey.from_private_key_file(pkey)]
        return pass_list
    def run_cmd(self,cmd):
        stdin,stdout,stderr = self.obj.exec_command(cmd)
        return [std.strip().encode("utf-8") for std in stdout.readlines()]
    def run_cmd_info(self,cmd):
        stdin, stdout, stderr = self.obj.exec_command(cmd)
        return ([std.strip().encode("utf-8") for std in stdout.readlines()],[std.strip().encode("utf-8") for std in stderr.readlines()])

    def run_cmdlist(self,cmdlist):
        self.resultList = []
        for cmd in cmdlist:
            stdin,stdout,stderr = self.obj.exec_command(cmd,timeout=self.timeout)
            result=[std.strip().encode("utf-8") for std in stdout.readlines()]
            self.logger.warning("command:{0} exec over as result:{1}".format(cmd,result))
            self.resultList.append(result)
            time.sleep(1)
        return self.resultList

    def get(self,remotepath,localpath):
        self.objsftp.get(remotepath,localpath)

    def put(self,localpath,remotepath):
        self.objsftp.put(localpath,remotepath)

    def getTarPackage(self,path):
        list = self.objsftp.listdir(path)
        for packageName in list:
            stdin,stdout,stderr  = self.obj.exec_command("cd " + path +";"
                                                         + "tar -zvcf /tmp/" + packageName
                                                         + ".tar.gz " + packageName)
            stdout.read()
            self.objsftp.get("/tmp/" + packageName + ".tar.gz","/tmp/" + packageName + ".tar.gz")
            self.objsftp.remove("/tmp/" + packageName + ".tar.gz")
            self.logger.info("get package from " + packageName + " ok......")

    def close(self):
        try:
            if self.obj:
                self.objsftp.close()
                self.obj.close()
        except Exception as e:
            self.logger.error(e)
    def __enter__(self):
        return self
    def __exit__(self,type,value,trace):
        if type or value or trace:
            self.logger.error("trpe:{0},value:{1},trace:{2}".format(type,value,trace))
        self.close()
if __name__ == '__main__':
    sshobj = myParamiko('10.10.8.21','root','xxxxxxxx',22)
    sshobj.close()