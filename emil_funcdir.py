from emil_vardir import *
import json

class FuncDir:
    def __init__(self):
        self.funcs = {}

    def add_func(self, name = None, ret = None, varc = None, paramcount = None, params = None, vart = None, addr = None, quad = None,
                 var = None):
        self.funcs[name] = FuncDirEntry(ret, varc, paramcount, params, vart, addr, quad,
                 var)

    def get_func(self, name):
        return self.funcs[name]

    def get_func_addr(self, name):
        return self.funcs[name].addr
    
    def check_if_func_exists(self, name):
        return name in self.funcs
    
    def get_func_quad(self, name):
        return self.funcs[name].quad
    
    def get_func_type(self, name):
        return self.funcs[name].ret
    
    def set_vardir(self, name, vardir):
        self.funcs[name].var = vardir

    def set_paramcont(self, name, cont):
        self.funcs[name].paramcount = cont

    def check_arg_type(self, name, tipo, pos):
        if(pos > self.funcs[name].paramcount):
            raise Exception("ERROR - Too many arguments")
        return self.funcs[name].params[pos] == tipo
    
    def get_paramcount(self, name):
        return self.funcs[name].paramcount
    
    def check_param_count(self,name,kant):
        return self.funcs[name].paramcount == kant
    
    def incrementar_param_cont(self, name, tipo):
        self.funcs[name].params.append(tipo)
        
    def get_vardir(self, name):
        return self.funcs[name].var
    
    def set_varcont(self, name):
        self.funcs[name].varc = self.funcs[name].var.var_count() - self.funcs[name].paramcount
    
    def set_quadcont(self, name, quadstart):
        self.funcs[name].quad = quadstart

    def set_vart(self, name, cont):
        self.funcs[name].vart = cont

    def get_size(self, name):
       return sum(self.funcs[name].vart) + self.funcs[name].varc + self.funcs[name].paramcount
    
    def print(self):
        for func in self.funcs:
            print(func, self.funcs[func])

    def __str__(self):
        return json.dumps([{k: json.loads(str(v))} for k, v in self.funcs.items()], indent = 2)


class FuncDirEntry:
    def __init__(self, ret, varc, paramcount, params, vart, addr, quad,
                 var):
        self.ret = ret  #return type
        self.varc = varc  #count of variables (how many variables it has)
        self.paramcount = paramcount  #count of parameters
        self.params = params  #list of parameters
        self.vart = vart  #count of temporary variables
        self.addr = addr  #direccion de memoria para el return
        self.quad = quad  #direccion del cuadruplo
        self.var = var  #pointer to the variable directory

    def __str__(self):
        # params = None
        
        # try:
        #     params = [json.loads(str(i)) for i in self.params]
        # except:
        #     pass
        
        return json.dumps({
            'ret': self.ret,
            'varc': self.varc,
            'paramcount': self.paramcount,
            'params': self.params,
            'vart': self.vart,
            'addr': self.addr,
            'quad': self.quad,
            'var': json.loads(str(self.var))
        })
