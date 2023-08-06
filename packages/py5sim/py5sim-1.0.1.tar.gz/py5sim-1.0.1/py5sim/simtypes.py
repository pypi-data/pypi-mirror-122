class Status:
    CANCEL = -1
    SEND = 1
    COMPLITE = 6
    BUSY = 10

class Struct:
    def __init__(self, *args, **entries):
        main_dict = {}
        for a in args:
            if type(a) == dict:
                main_dict.update(a)
        
        main_dict.update(entries)
        
        self.__dict__.update(main_dict)
        for k, v in self.__dict__.items():
            if type(v) == dict:
                self.__dict__[k] = Struct(**v)
            elif type(v) == list:
                self.__dict__[k] = []
                for m in v:
                    if type(m) == dict:
                        self.__dict__[k].append(Struct(**m))
                    else:
                        self.__dict__[k].append(m)
                        
                    
    
    def __repr__(self):
        return str(self.__dict__)
    
    def __str__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
      
    def __getattr__(self, item):
        return None

    def __getitem__(self, item):
        return self.get(item)
    
    def __setitem__(self, item, value):
        self.__dict__[item] = value
    
    def items(self):
        return self.__dict__.items()
    
    def get(self, key):
        return self.__dict__.get(key)

class SimResponse(Struct):
    pass

class UserResponse(Struct):
    pass

class GuestResponse(Struct):
    pass

class ApiKeyError(Exception):
    pass

class AuthorizationError(Exception):
    pass