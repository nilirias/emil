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

    def get_func_quad(self, name):
        return self.funcs[name].quad
    
    def get_func_type(self, name):
        return self.funcs[name].ret
    
    def set_vardir(self, name, vardir):
        self.funcs[name].var = vardir

    def get_vardir(self, name):
        return self.funcs[name].var

    def __str__(self):
        #print('vardir.__str__', json.dumps([str(i) for i in self.vars]))
        return json.dumps([i for i in self.funcs])
        #return json.dumps([json.loads(str(i)) for i in self.funcs])


class FuncDirEntry:
    def __init__(self, ret, varc, paramcount, params, vart, addr, quad,
                 var):
        self.ret = ret  #return type | 0 for main | 1 for void | 2 for number | 3 for word | 4 for bool
        self.varc = varc  #count of variables (how many variables it has) [numbers, words, bools]
        self.paramcount = paramcount  #count of parameters
        self.params = params  #list of parameters
        self.vart = vart  #count of temporary variables
        self.addr = addr  #direccion de memoria para el return
        self.quad = quad  #direccion del cuadruplo
        self.var = var  #pointer to the variable directory

    def __str__(self):
        # print('vardirentry.__str__', json.dumps({'name': self.name, 'addr': self.addr}))
        #print('vardirentry.__str__', json.dumps({'name': self.name, 'ret': self.ret, 'varc': self.varc, 'params': self.params, 'vart': self.vart, 'addr': self.addr, 'var': str(self.var)}))
        return json.dumps({
            'ret': self.ret,
            'varc': self.varc,
            'paramcount': self.paramcount,
            'params': json.dumps([json.loads(str(i)) for i in self.params]),
            'vart': self.vart,
            'addr': self.addr,
            'quad': self.quad,
            'var': json.loads(str(self.var))
        })
