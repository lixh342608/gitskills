#coding=utf-8

import paramiko,os,time,configparser

from prometheus_client import CollectorRegistry,Gauge,push_to_gateway

from multiprocessing import process,Queue,Event

import configparser,sys,random,string
sys.path.append('../')
from until_funtion.ssh_tool import ssh_tool
from until_funtion.globallogger import globallogger

class collection_data():
    config=configparser.ConfigParser()
    cur_path=os.path.dirname(os.path.realpath(__file__))
    config_path=os.path.join(cur_path,"monitor_config.ini")
    config.read(config_path)
    def __init__(self):
        self.logger=self.get_logger()
        self.nodes=self.config.items("nodes")
        self.node_list=[node[1] for node in self.nodes]
        self.small_node=self.config.items("smallnodes")
        self.small_node_list = [node[0] for node in self.small_node]
        self.small_node_dic=dict(self.small_node_list)
        self.small_user=self.config.get("default","small_user")
        self.ssh_tool=ssh_tool(logger=self.logger)
    def get_logger(self):
        log_file=os.path.join(self.cur_path,"collection_data.log")
        logger_handle=globallogger("collection",log_file=log_file)
        return logger_handle.log
    def get_cpu_info(self,node):
        data_type="systemcpu"
        data_dic={"keyword":data_type+"_used",
                  "job":node+"_"+data_type,
                  "lables":["sys_name","sys_type"],
                  "value_list":[]
                  }
        cpu_command = "top -bn 1|sed -n '3p'| awk -F ':' '{print $2}'|awk '{print $1}'"
        if "_" in node:
            password=self.small_node_dic.get(node)
            node_list=node.split("_")
            node=node_list[0]
            node_ip=node_list[1]
            cpu_command ="""sshpass -p "%s" ssh %s@%s "export PATH=/usr/sbin:$path;%s" """ % (password,self.small_user,node_ip,cpu_command)
        cpu_use=self.exec_command(cpu_command,node)
        data_dic["value_list"].append([data_type,data_type,cpu_use[0].replace("%","")])
        return data_dic
    def get_mem_info(self,node):
        data_type = "systemmem"
        data_dic={"keyword":data_type+"_used",
                  "job":node+"_"+data_type,
                  "lables":["sys_name","sys_type"],
                  "value_list":[]
                  }
        mem_command = """free -m|sed -n '2p' |awk '{printf ("%.1f\\n",$3/$2*100)}'"""
        if "_" in node:
            password=self.small_node_dic.get(node)
            node_list=node.split("_")
            node=node_list[0]
            node_ip=node_list[1]
            mem_command ="""sshpass -p "%s" ssh %s@%s "export PATH=/usr/sbin:$path;%s" """ % (password,self.small_user,node_ip,mem_command)
        mem_use = self.exec_command(mem_command, node)
        data_dic["value_list"].append([data_type,data_type,mem_use[0].replace("%","")])

        return data_dic
        
