import json

class CteDir:
  def __init__(self):
        self.cte = []
     
  def add_cte(self, name, addr):
      self.cte.append(CteDirEntry(name, addr))

  def __str__(self):
    return json.dumps([json.loads(str(i)) for i in self.cte])

class CteDirEntry:
    def __init__(self, name, addr):
        self.name = name  #variable name
        self.addr = addr  #address

    def __str__(self):
        return json.dumps({'name': self.name, 'addr': self.addr})
