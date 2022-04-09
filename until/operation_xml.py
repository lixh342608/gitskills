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
    def isincludedict(self,ind,oud):
        ind_set=set(ind.items())
        oud_set = set(oud.items())
        if ind_set.issubset(oud_set):
            return True
        return False
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
            for node in nodes:
                if self.isincludedict(attr_map,node.attrib):
                    return node
        else:
            return self.findfirstnode(paths,parentnode=parentnode)
        return None
    def add_chaildtag(self,tagname,tagtext="",tagattr={},parentnode=None):
        if not parentnode:
            parentnode=self.root
        newchaild=ET.Element(tagname,tagattr)
        newchaild.text=tagtext
        parentnode.append(newchaild)
    def changeattr(self,attrs={},parentnode=None,is_delete=False):
        if not attrs:
            return
        nodelist=parentnode
        if not parentnode:
            nodelist=[self.root]
        elif isinstance(parentnode,str):
            nodelist=[parentnode]
        for node in nodelist:
            for attr in attrs.keys():
                if is_delete:
                    if attr in node.attrib.keys():
                        del node.attrib[attr]
                else:
                    node.set(attr,attrs.get(attr))
    def changetext(self,text="",parentnode=None,is_add=False,is_delete=False):
        nodelist=parentnode
        if not parentnode:
            nodelist=[self.root]
        elif isinstance(parentnode,str):
            nodelist=[parentnode]
        for node in nodelist:
            if is_add:
                node.text+=text
            elif is_delete:
                node.text=""
            else:
                node.text = text
    def delnode_bytagattr(self,tags=None,parentnode=None,attrs={}):
        if parentnode == None:
            parentnode=self.root
        if not tags:
            return
        tags=self.full_path(tags)
        for childnode in list(parentnode):
            if childnode.tag == tags and self.isincludedict(attrs,childnode.attrib):
                    parentnode.remove(childnode)

    def prettyXml(self,element, indent="\t", newline="\n", level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
        if element:  # 判断element是否有子元素
            if element.text == None or element.text.isspace():  # 如果element的text没有内容
                element.text = newline + indent * (level + 1)
            else:
                element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
                # else: # 此处两行如果把注释去掉，Element的text也会另起一行
            # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
        temp = list(element)  # 将elemnt转成list
        for subelement in temp:
            if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
                subelement.tail = newline + indent * (level + 1)
            else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
                subelement.tail = newline + indent * level
            self.prettyXml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作
    def savexml(self):
        self.prettyXml(self.root)
        self.write(self.xml_file,encoding="utf-8",xml_declaration=True,method="xml")
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.savexml()

if __name__ == "__main__":
    with operation_xml("log.xml") as xmls:
        xmls.delnode_bytagattr(tags="appender",attrs={})
    #xmls=operation_xml("log.xml")
    #print(xmls.isincludedict({"a":"b"},{}))
    #nodes=xmls.findsinglenode("appender",attr_map={"name":"DIALOG"})
    #print(nodes.text)

