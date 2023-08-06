import importlib
import os
import re
import sys
import pathlib

import open3d as o3d

import cv2

from hito.func.engine.hitoFunc import HitoFunc
from hito.func.utils.parameter import getFuncArgumens


class FuncLoader():
    def __init__(self,path):
        self.funcFactory={}
        pass
    def createInstance(self,module_name, class_name, *args, **kwargs):
        module_meta = __import__(module_name, globals(), locals(), [class_name])
        class_meta = getattr(module_meta, class_name)
        obj = class_meta(*args, **kwargs)
        return obj


    #扫描对应路径加载类，基类为HitoFunc
    def scan(self,path):
        #if name in sys.modules:
        #    print(f"{name!r} already in sys.modules")
        try:
            file_list = os.listdir(path)
        except:
            file_list = []
            print("the path is not dir")
        if file_list:
            for file in file_list:
                file = os.path.join(path, file)
                print(file)
                if os.path.isdir(file):
                    self.scan(file)
                else:
                    if file.endswith(".py"):
                        with open(file, encoding="utf-8") as f:
                            for line in f.readlines():
                                cls_match = re.match(r"class\s(.*?)[\(:]", line)
                                if cls_match:
                                    cls_name = cls_match.group(1)
                                    model_name=pathlib.Path(file).stem
                                    try:
                                        loader = importlib.machinery.SourceFileLoader(model_name, file)
                                        spec = importlib.util.spec_from_loader(loader.name, loader)
                                        mod = importlib.util.module_from_spec(spec)
                                        sys.modules[model_name] = mod
                                        spec.loader.exec_module(mod)
                                        #mod = types.ModuleType(loader.name)
                                        #mod = loader.exec_module(mod)
                                        cls_a = getattr(mod, cls_name)
                                        instance = cls_a()
                                        if  isinstance(instance,HitoFunc):
                                            #if self.funcFactory.get(cls_name) == None:
                                            self.funcFactory[cls_name]=instance
                                    except:
                                         pass

    def getFunc(self, className):
        if className in self.funcFactory:
            return self.funcFactory[className]
        else:
            raise Exception("类{}未找到",className)


if __name__ == '__main__':
    loader = FuncLoader("")
    loader.scan(r"C:\test\htfunc\test")
    #hitoFunc =loader.createInstance("func.test.customFunc","CustomFunc")

    hitoFunc = loader.getFunc("CustomFunc")
    var = {"num5": 1, "num2": 2, "num3": 3, "num4": 4}
    print(hitoFunc.__class__.__name__,hitoFunc.process(**var))


    var3 = {"num1": 1, "num2": 2, "num3": 3, "num4": 5}
    hitoFunc = loader.getFunc("Custom2Func")
    print(hitoFunc.__class__.__name__, hitoFunc.process(**var3))



    var3 = {"num1": 1, "num2": 2, "num3": 3, "num4": 6}
    hitoFunc = loader.getFunc("Custom3Func")
    print(hitoFunc.__class__.__name__, hitoFunc.process(**var3))

    im1 = cv2.imread(r"..\..\3-23.jpg")
    im2 = cv2.imread(r"..\..\3-23.jpg")
    hitoFunc = loader.getFunc("EccAlignFunc")
    var3 = {"im1": im1, "im2": im2}
    #print(hitoFunc.__class__.__name__, getFuncArgumens(hitoFunc.process))
    print(hitoFunc.__class__.__name__, hitoFunc.process(**var3))

    source = o3d.t.io.read_point_cloud(r'..\..\RH\tr\pcd_tr_1-1_YGJ-bolt_1.pcd')
    target = o3d.t.io.read_point_cloud(r'..\..\RH\ref\pcd_ref_1-1_YGJ-bolt_1.pcd')
    hitoFunc = loader.getFunc("MultiScaleIcpAlignFunc")
    var3 = {"source": source, "target": target}
    #print(hitoFunc.__class__.__name__, getFuncArgumens(hitoFunc.process))
    print(hitoFunc.__class__.__name__,hitoFunc.process(**var3).transformation )

    #draw_registration_result(source.cpu(), target.cpu(),
        #                         registration_ms_icp.transformation)