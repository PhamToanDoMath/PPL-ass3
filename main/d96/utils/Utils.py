
class Utils:
    def lookup(self,name,lst,func):
        for x in lst:
            # print(name, func(x))
            if name == func(x):
                # print('Accept')
                return x
        return None

