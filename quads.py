class Quadruple:

  def __init__(self, lo, ro, op, res):
    self.lo = lo
    self.ro = ro
    self.op = op
    self.res = res

  def __str__(self):
    return f'{self.op} {self.lo} {self.ro} {self.res}'
