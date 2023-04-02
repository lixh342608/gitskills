#coding=utf-8

from ruamel import yaml
from pathlib import Path
codes="utf-8"

class easy_yaml():
    def __init__(self,yaml_file,output_file=None):
        self.yaml_file=Path(yaml_file)
        self.output_file=output_file
        self.data=self.read_yaml()
        self._value=lambda x,d,s:s if isinstance(x[1],int) else d.get(x[0])
        self.get_data = lambda data:data if data else self.data
        self.get_address = lambda p:p if isinstance(p,list) else [p,0]
    def read_yaml(self):
        st=self.yaml_file.open("r",encoding=codes)
        return yaml.round_trip_load(st)

    def get_value(self,path_address,data=None):
        data=self.get_data(data)
        rdata=None
        if isinstance(data,dict) :
            if isinstance(path_address,str):
                rdata = data.get(path_address)
        elif isinstance(data,list):
            path_address = self.get_address(path_address)
            snum=0
            for index,obj in enumerate(data):
                if isinstance(path_address,list) and len(path_address) ==2:
                    if path_address[0] in obj.keys():
                        subv=self._value(path_address,obj,snum)
                        if subv==path_address[1]:
                            rdata=obj
                            break
                        snum+=1
        return rdata

    def get_values(self,path_address,data=None):
        data=self.get_data(data)
        if isinstance(path_address,list) and path_address:
            if len(path_address) == 1:
                return self.get_value(*path_address,data)
            else:
                data=self.get_value(path_address[0],data)
                return self.get_values(path_address[1:],data)
        elif isinstance(path_address,str):
            return self.get_value(path_address, data)
    def set_value(self,path_address,new_value,old_value=None,data=None):
        data = self.get_data(data)
        if isinstance(data,dict):
            if isinstance(path_address,str):
                res=self.get_value(path_address,data)
                if isinstance(res, str):
                    if old_value is None:
                        old_value = res.strip()
                    data[path_address]=res.replace(old_value,new_value)
                else:
                    data[path_address]=new_value
        elif isinstance(data,list):
            path_address = self.get_address(path_address)
            snum=0
            for index, obj in enumerate(data):
                if isinstance(path_address, list) and len(path_address) == 2:
                    if path_address[0] in obj.keys():
                        subv=self._value(path_address,obj,snum)
                        if subv==path_address[1]:
                            rdata=self.set_value(path_address[0],new_value,old_value=old_value,data=obj)
                            data[index]=rdata
                            break
                        snum+=1
            else:
                if isinstance(path_address[1],int):
                    data.insert(path_address[1],new_value)
                else:
                    data.append(new_value)
        return data
    def _set_values(self,path_address,new_value,old_value=None,data=None):
        data = self.get_data(data)
        if isinstance(path_address,list) and path_address:
            if len(path_address) == 1:
                data = self.set_value(*path_address,new_value,old_value=old_value,data=data)
            else:
                child_data=self.get_value(path_address[0],data)
                new_child_data=self._set_values(path_address[1:],new_value,old_value=old_value,data=child_data)
                data = self.set_value(path_address[0],new_child_data,old_value=child_data,data=data)
        elif isinstance(path_address,str):
            data=self.set_value(path_address,new_value,old_value=old_value,data=data)
        return data
    def set_values(self,path_address,new_value,old_value=None):
        self.data=self._set_values(path_address,new_value,old_value=old_value)
    def del_value(self,path_address,data=None):
        data=self.get_data(data)
        if isinstance(data,dict):
            if isinstance(path_address,str):
                data.pop(path_address)
        elif isinstance(data,list):
            path_address=self.get_address(path_address)
            snum=0
            for index, obj in enumerate(data):
                if isinstance(path_address, list) and len(path_address) == 2:
                    if path_address[0] in obj.keys():
                        subv=self._value(path_address,obj,snum)
                        if subv==path_address[1]:
                            data.remove(obj)
                            break
                        snum+=1
        return data
    def _del_values(self,path_address,data=None):
        data = self.get_data(data)
        if isinstance(path_address, list) and path_address:
            if len(path_address) == 1:
                data = self.del_value(*path_address, data=data)
            else:
                child_data = self.get_value(path_address[0], data)
                new_child_data = self._del_values(path_address[1:], data=child_data)
                data = self.set_value(path_address[0], new_child_data, old_value=child_data, data=data)
        elif isinstance(path_address, str):
            data = self.del_value(path_address,data=data)
        return data
    def del_values(self, path_address):
        self.data = self._del_values(path_address)
    def write_yml(self):
        if self.output_file is None:
            self.output_file = self.yaml_file
        st=Path(self.output_file).open("w",encoding=codes)
        yaml.round_trip_dump(self.data,st,allow_unicode=True,width=1000,default_flow_style=False)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.write_yml()

if __name__ == "__main__":
    yamls=easy_yaml("test.yml")

