from abc import abstractmethod
from enum import Enum

#from hito.func.utils.parameter import getFuncArgumens

class FuncType(Enum):
    INPUT=1
    PREPPROCESS=2
    PROCESS=3
    CONDITION=4
    OUTPUT=5

class HitoFunc():
    @abstractmethod
    def process(self, **kwargs): #处理入口函数
        pass


    @abstractmethod
    def getFuncType(self)->FuncType: #函数类型说明
        pass


    @abstractmethod
    def getArgumentsDefine(self):#函数参数说明
        pass
        #getFuncArgumens(self.process)


    @abstractmethod
    def getBranchDefine(self): # 函数输出分支定义
        return 'DEFAULT'


    @abstractmethod
    def getExample(self): #配置示例说明
       pass
       
    @abstractmethod
    def getFuncName(self): #函数中文说明用于前端展示
       pass


