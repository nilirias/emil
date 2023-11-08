import json

class VarDir:
    def __init__(self):
        self.vars = []

    def add_var(self, name, addr, type):
        if all(entry.name != name for entry in self.vars):
            self.vars.append(VarDirEntry(name, addr, type))

    def get_var(self, name):
        x = [var for var in self.vars if var.name == name]
        return x[0] if len(x) > 0 else None

    def var_count(self):
        return len(self.vars)
    
    def check_if_var_exists(self, name):
        return len([var.addr for var in self.vars if var.name == name]) > 0

    def get_var_address(self, name):
        return [var.addr for var in self.vars if var.name == name][0]

    def __str__(self):
        return json.dumps([json.loads(str(i)) for i in self.vars])


class VarDirEntry:

    def __init__(self, name, addr, type):
        self.name = name  #variable name
        self.addr = addr  #address
        self.type = type

    def get_addr(self):
        return self.addr
    
    def get_type(self):
        return self.type

    def __str__(self):
        return json.dumps({
            'name': self.name,
            'addr': self.addr,
            'type': self.type
        })
