import json

class CteDir:
    def __init__(self):
        self.cte = []
    
    def add_cte(self, value, addr, vartype):
        if all(entry.value != value for entry in self.cte):
            self.cte.append(CteDirEntry(value, addr, vartype))
            return True
        return False

    def get_entry(self, value):
        x = [i for i in self.cte if i.value == value]
        return x[0] if len(x) > 0 else None

    def __str__(self):
        return json.dumps([json.loads(str(i)) for i in self.cte])

class CteDirEntry:
    def __init__(self, value, addr, vartype):
        self.value = value  #variable name
        self.addr = addr  #address
        self.vartype = vartype #vartype
    
    def get_value(self):
        return self.value

    def get_type(self):
        return self.vartype

    def __str__(self):
        return json.dumps({'name': self.value, 'addr': self.addr, 'vartype': self.vartype})
