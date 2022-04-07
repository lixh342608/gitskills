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
        print(self.root)
    def get_namespace(self):
        namespace=dict([node for _,node in ET.iterparse(self.xml_file,events=["start-ns"])])
        if not namespace:
            self.namespace=""
        else:
            self.namespace="{%s}" % namespace.get("")
        for ns in namespace:
            ET.register_namespace(ns,namespace[ns])

if __name__ == "__mani__":
    xmls=operation_xml("neox.xml")
    print(ET.tostring(xmls.root))

