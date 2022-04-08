#coding=utf-8
from xml.etree import ElementTree as ET


class commentbuilder(ET.TreeBuilder):
    def __init__(self,*args,**kwargs):
        super(commentbuilder, self).__init__(*args,**kwargs)
    def comment(self,data):
        self.start(ET.Comment,{})
        self.data(data)
        self.end(ET.Comment)
class operation_xml(ET.ElementTree):
    def __init__(self,xml_file):
        self.xml_file = xml_file
        super(operation_xml, self).__init__()
        self.get_namespace()
        parser=ET.XMLParser(target=commentbuilder())
        self.parse(self.xml_file,parser=parser)
        self.root=self.getroot()
    def get_namespace(self):
        namespace=dict([node for _,node in ET.iterparse(self.xml_file,events=["start-ns"])])
        self.namespace = ""
        if namespace.get("") != None:
            self.namespace = "{%s}" % namespace.get("")
        for ns in namespace:
            ET.register_namespace(ns,namespace[ns])
    def full_path(self,paths):
        path_list=paths.split("/")
        path_list=[self.namespace+path for path in path_list]
        path="/".join(path_list)
        return path
    def findfirstnode(self,paths,parentnode=None):
        if not parentnode:
            parentnode=self.root
        paths=self.full_path(paths)
        return parentnode.find(paths)
    def findallnode(self,paths,parentnode=None):
        if not parentnode:
            parentnode=self.root
        paths=self.full_path(paths)
        return parentnode.findall(paths)
    def findsinglenode(self,paths,chaildtag=None,text=None,attr_map=None,parentnode=None):
        if parentnode == None:
            parentnode=self.root
        nodes=self.findallnode(paths,parentnode=parentnode)
        if isinstance(chaildtag,str):
            for node in nodes:
                tags=[nd.tag for nd in list(node)]
                if chaildtag in tags:
                    return node
        elif isinstance(text,str):
            for node in nodes:
                if text == node.text:
                    return node
        elif isinstance(attr_map,dict):
            attr_set = set(attr_map.items())
            for node in nodes:
                node_set = set(node.attrib.items())
                if attr_set.issubset(node_set):
                    return node
        else:
            return self.findfirstnode(paths,parentnode=parentnode)
        return None






if __name__ == "__main__":
    xmls=operation_xml("log.xml")
    nodes=xmls.findfirstnode("appender")
    print([node.tag for node in list(nodes)])

