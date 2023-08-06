

#定义节点信息
from typing import List


class NodeParentInfo():
    def __init__(self,parentId,branch='DEFAULT'):
        self.__parentId=parentId
        self.__branch = branch

    def __str__(self):
        """返回一个对象的描述信息"""
        # print(num)
        return "父节点是:%s , 分支是:%s" % (self.parentId, self.branch)

    def __repr__(self):
        return self.__str__()

    @property
    def parentId(self):
        return self.__parentId

    @property
    def branch(self):
        return self.__branch



class NodeInfo():
    def __init__(self,nodeId,func_name,arguments,parents:List[NodeParentInfo]=[ ]):
        self.__nodeId=nodeId
        self.__funcName=func_name
        self.__arguments=arguments
        self.__parents=parents

    @property
    def nodeId(self):
        return self.__nodeId

    @property
    def funcName(self):
        return self.__funcName

    @property
    def arguments(self):
        return self.__arguments

    @property
    def  parents(self):
        return self.__parents



    def __str__(self):
        return "节点是:%s,函数名字:%s,参数信息:%s,父节点信息:%s" % (self.nodeId,self.funcName,self.arguments,''.join(self.parents.__repr__()))

    def __repr__(self):
        return self.__str__()

if  __name__ == '__main__':
    nodeParent =NodeParentInfo("n1")
    print(nodeParent.branch)
    print(nodeParent)

    node1=NodeInfo("n1","readImg",r"..\..\3-23.jpg")
    print(node1)

    node2=NodeInfo("n2","yolov5","ls_lm_weight.pt,0.6",[nodeParent])
    print(node2)

    nodeParent2 =NodeParentInfo("n2")
    print(nodeParent)

    node3=NodeInfo("n3","writeReulst","det",[nodeParent2])
    print(node3)