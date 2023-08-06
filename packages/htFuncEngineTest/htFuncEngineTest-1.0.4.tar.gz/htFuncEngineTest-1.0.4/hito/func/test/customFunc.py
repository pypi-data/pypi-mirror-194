from hito.func.engine.hitoFunc import HitoFunc



#不能被加载
class ErrorCustomFunc():
    def process(self, num5, num2, *, num3, num4=5):
        return num5 + num2 + num3 + num4

class CustomFunc(HitoFunc):
    def process(self, num5, num2, *, num3, num4=5):
        return num5 + num2 + num3 + num4

class Custom2Func(HitoFunc):
    def process(self, num1, num2, **num3):
        total = num1 + num2
        for k, v in num3.items():
            total += v
        return total


class Custom3Func(HitoFunc):
    def process(self, num1: int, num2: int, **num3: dict) -> int:
        total = num1 + num2
        for k, v in num3.items():
            total += v
        return total
