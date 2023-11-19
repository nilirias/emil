from sly import Parser
from sly.yacc import _decorator as _
from emil_lexer import EmilLexer
from emil_funcdir import FuncDir
from emil_vardir import VarDir
from emil_cte import CteDir
from quads import Quadruple
from emil_semanticcube import rel_ops, eq_ops, log_ops, checkOperator
import sys


class EmilParser(Parser):
  tokens = EmilLexer.tokens
  quadList = []
  stackOperadores = []
  stackOperandos = []
  stackTypes = []
  stackJumps = []
  tempCont = 1
  quadCont = 1
  paramCont = 0
  varlclCont = 0
  debugfile = 'debug.txt'
  directorioProcedimientos = None
  scopeName = None
  currType = None
  currVar = None
  programName = None
  funcType = None
  cteDir = CteDir()

  intlcl = 0
  fltlcl = 1000
  charlcl = 2000
  boollcl = 3000
  
  intglb = 4000
  fltglb = 5000
  charglb = 6000
  boolglb = 7000

  inttemp = 8000
  flttemp = 9000
  chartemp = 10000
  booltemp = 11000

  intcte = 12000
  fltcte = 13000
  charcte = 14000
  boolcte = 15000

  def genQuad(self):
    typeaddr = None
    rightOp = self.stackOperandos.pop()
    rightType = self.stackTypes.pop()
    leftOp = self.stackOperandos.pop()
    leftType = self.stackTypes.pop()
    op = self.stackOperadores.pop()

    checkOp = checkOperator(rightType, leftType, op)
    
    if (op == '='):
      self.quadList.append(Quadruple(leftOp, rightOp, op, ''))
      self.stackTypes.append(checkOp)
      self.quadCont += 1
    else:
      if (checkOp == 'int'):
        typeaddr = self.inttemp
        self.inttemp += 1
      elif (checkOp == 'float'):
        typeaddr = self.flttemp
        self.flttemp += 1
      elif (checkOp == 'char'):
        typeaddr = self.chartemp
        self.chartemp += 1
      elif (checkOp == 'bool'):
        typeaddr = self.booltemp
        self.booltemp += 1
    
      self.quadList.append(Quadruple(leftOp, rightOp, op, typeaddr))
      self.quadCont += 1
      self.stackOperandos.append(typeaddr)
      self.stackTypes.append(checkOp)
      self.tempCont += 1

    return self.quadList[-1].res
    #print(checkOp)

  def checkVarExists(self, x):
    aux = self.directorioProcedimientos.get_vardir(self.scopeName).get_var(x)
    #Check de variables locales
    if (aux != None):
      return aux
    #Check de variables locales
    aux = self.directorioProcedimientos.get_vardir(self.programName).get_var(x)
    if (aux != None):
      return aux
    else:
      raise Exception("ERROR - Variable no declarada")

  @_('PROGRAM prog1 ID prog2 SEMICLN varsdecl funcdecl main')
  def program(self, p):
    for idx, quad in enumerate(self.quadList, 1):
      print(idx, quad)
    print(self.directorioProcedimientos)
    print(self.cteDir)
    return 69

  @_('')
  def prog1(self, p):
    self.directorioProcedimientos = FuncDir()
    self.quadList.append(Quadruple('', '', 'GOTO', ''))
    self.quadCont +=  1

  @_('')
  def prog2(self, p):
    self.directorioProcedimientos.add_func(name=p[-1])
    self.scopeName = p[-1]
    self.programName = p[-1]

  @_('VARS prog3 multivd multid', 'empty')
  def varsdecl(self, p):
    return 0

  @_('')
  def prog3(self, p):
    if(self.directorioProcedimientos.get_vardir(self.scopeName) == None):
      varDirProg = VarDir()
      self.directorioProcedimientos.set_vardir(self.scopeName, varDirProg)

  @_('tipo prog4 COLON ID prog5 arr multid SEMICLN multivd', 'empty')
  def multivd(self, p):
    return 0

  @_('')
  def prog4(self, p):
    self.currType = p[-1]

  @_('')
  def prog5(self, p):
    self.currVar = self.directorioProcedimientos.get_vardir(self.scopeName)
    if (self.currVar.get_var(p[-1]) != None):
      raise Exception("ERROR - Variable already declared")
    if(self.scopeName == self.programName): #variable global
      if (self.currType == 'int'):
        self.currVar.add_var(p[-1], self.intglb, self.currType)
        self.intglb += 1
      elif(self.currType == 'float'):
        self.currVar.add_var(p[-1], self.fltglb, self.currType)
        self.fltglb += 1
      elif(self.currType == 'char'):
        self.currVar.add_var(p[-1], self.charglb, self.currType)
        self.charglb += 1
      elif(self.currType == 'bool'):
        self.currVar.add_var(p[-1], self.boolglb, self.currType)
        self.boolglb += 1
    else:
      if (self.currType == 'int'):
        self.currVar.add_var(p[-1], self.intlcl, self.currType)
        self.intlcl += 1
      elif(self.currType == 'float'):
        self.currVar.add_var(p[-1], self.fltlcl, self.currType)
        self.fltlcl += 1
      elif(self.currType == 'char'):
        self.currVar.add_var(p[-1], self.charlcl, self.currType)
        self.charlcl += 1
      elif(self.currType == 'bool'):
        self.currVar.add_var(p[-1], self.boollcl, self.currType)
        self.boollcl += 1

  @_('COMMA ID prog5 arr multid', 'empty')
  def multid(self, p):
    return 0

  @_('INT', 'FLOAT', 'CHAR', 'BOOL')
  def tipo(self, p):
    return p[0]

  @_('LSQUARE exp RSQUARE', 'empty')
  def arr(self, p):
    return 0

  @_('FUNC tipofunc func1 ID func2 LPAREN param RPAREN func3 LCURLY varsdecl func4 stmnt RCURLY resetvarcont funcdecl',
     'empty')
  def funcdecl(self, p):
    return 0

  @_('')
  def func1(self, p):
    self.funcType = p[-1]
    
  @_('')
  def func2(self, p):
    self.directorioProcedimientos.add_func(name = p[-1], ret = self.funcType, var = VarDir())
    self.scopeName = p[-1]

  @_('')
  def func3(self,p):
    self.directorioProcedimientos.set_paramcont(self.scopeName, self.paramCont)

  @_('')
  def func4(self, p):
    self.directorioProcedimientos.set_varcont(self.scopeName)
    self.directorioProcedimientos.set_quadcont(self.scopeName, self.quadCont)

  @_('')
  def resetvarcont(self, p):
    self.paramCont = 0
    #self.directorioProcedimientos.set_vardir(self.scopeName, None)
    vartemps = [self.inttemp - 8000, self.flttemp - 9000, self.chartemp - 10000, self.booltemp - 11000]  
    self.directorioProcedimientos.set_vart(self.scopeName, vartemps)

    self.intlcl = 0
    self.fltlcl = 1000
    self.charlcl = 2000
    self.boollcl = 3000

    self.inttemp = 8000
    self.flttemp = 9000
    self.chartemp = 10000
    self.booltemp = 11000

  @_('VOID', 'tipo')
  def tipofunc(self, p):
    return p[0]

  @_('tipo param1 COLON ID param2 multiparam', 'empty')
  def param(self, p):
    return 0

  @_('')
  def param1(self, p):
    self.currType = p[-1]

  @_('')
  def param2(self, p):
    self.currVar = self.directorioProcedimientos.get_vardir(self.scopeName)
    if (self.currType == 'int'):
      self.currVar.add_var(p[-1], self.intlcl, self.currType)
      self.intlcl += 1
    elif(self.currType == 'float'):
      self.currVar.add_var(p[-1], self.fltlcl, self.currType)
      self.fltlcl += 1
    elif(self.currType == 'char'):
      self.currVar.add_var(p[-1], self.charlcl, self.currType)
      self.charlcl += 1
    elif(self.currType == 'bool'):
      self.currVar.add_var(p[-1], self.boollcl, self.currType)
      self.boollcl += 1
    self.paramCont += 1

  @_('COMMA param', 'empty')
  def multiparam(self, p):
    return 0

  @_('MAIN scopemain LPAREN RPAREN stmnt')
  def main(self, p):
    return 0
  
  @_('')
  def scopemain(self, p):
    self.scopeName = 'main'
    self.directorioProcedimientos.add_func(name = 'main', ret = 'main', var = VarDir())
    self.quadList[0].res = self.quadCont

  @_('ass_stmnt stmnt', 'func_stmnt stmnt', 'ret_stmnt stmnt',
     'read_stmnt stmnt', 'write_stmnt stmnt', 'if_stmnt stmnt',
     'while_stmnt stmnt', 'empty')
  def stmnt(self, p):
    return 0

  @_('ID ass1 arr ASS ass2 logic ass3 SEMICLN',
     'ID arr ASS func_stmnt SEMICLN')
  def ass_stmnt(self, p):
    return 0

  @_('')
  def ass1(self, p):
    aux = self.checkVarExists(p[-1])
    self.stackOperandos.append(aux.addr)
    self.stackTypes.append(aux.get_type())

  @_('')
  def ass2(self, p):
    self.stackOperadores.append(p[-1])

  @_('')
  def ass3(self, p):
    self.genQuad()

  @_('ID LPAREN arg RPAREN SEMICLN')
  def func_stmnt(self, p):
    return 0

  @_('logic multiarg', 'empty')
  def arg(self, p):
    return 0

  @_('COMMA arg multiarg', 'empty')
  def multiarg(self, p):
    return 0

  @_('RETURN LPAREN logic RPAREN SEMICLN')
  def ret_stmnt(self, p):
    return 0

  @_('READ io1 LPAREN logic multio io2 RPAREN io3 SEMICLN')
  def read_stmnt(self, p):
    return 0

  @_('WRITE io1 LPAREN logic io2 multio RPAREN io3 SEMICLN')
  def write_stmnt(self, p):
    return 0
  
  @_('COMMA logic io2 multio', '')
  def multio(self, p):
    pass
  
  @_('')
  def io1(self, p):
    #self.stackOperadores.append(p[-1])
    pass

  @_('')
  def io2(self, p):
    # resultado = self.stackOperadores[-1]
    # self.quadList.append(Quadruple('', '', resultado, p[-1]))
    # self.quadCont += 1
    pass

  @_('')
  def io3(self, p):
    #self.stackOperadores.pop()
    pass

  @_('rel log2', 'rel log2 AND log1 logic', 'rel log2 OR log1 logic')
  def logic(self, p):
    if(hasattr(p,'log1')):
      print('log', p.log2)
      return p.log2
    else:
      return p.log2

  @_('')
  def log1(self, p):
    self.stackOperadores.append(p[-1])

  @_('')
  def log2(self, p):
    if (len(self.stackOperadores) == 0):
      return p[-1]
    operadorTop = self.stackOperadores[-1]
    if (operadorTop in log_ops):
      return self.genQuad()
    return p[-1]

  @_('MORE_THAN', 'LESS_THAN', 'MORE_OR_EQ_THAN', 'LESS_OR_EQ_THAN',
     'DIFFERENT_TO', 'EQUAL_TO')
  def relop(self, p):
    return p[0]

  @_('exp rel2', 'exp rel2 relop rel1 rel')
  def rel(self, p):
    if(hasattr(p,'rel1')):
      print('rel', p.rel2)
      return p.rel2
    else:
      return p.rel2

  @_('')
  def rel1(self, p):
    self.stackOperadores.append(p[-1])

  @_('')
  def rel2(self, p):
    if (len(self.stackOperadores) == 0):
      return p[-1]
    operadorTop = self.stackOperadores[-1]
    if (operadorTop in rel_ops or operadorTop in eq_ops):
      return self.genQuad()
    return p[-1]

  @_('term exp2', 'term exp2 SUM exp1 exp', 'term exp2 SUB exp1 exp')
  def exp(self, p):
    if(hasattr(p,'exp1')):
      print('exp', p.exp2)
      return p.exp2
    else:
      return p.exp2

  @_('')
  def exp2(self, p):
    if (len(self.stackOperadores) == 0):
      return p[-1]
    operadorTop = self.stackOperadores[-1]
    if (operadorTop == '+' or operadorTop == '-'):
      return self.genQuad()
    return p[-1]

  @_('')
  def exp1(self, p):
    self.stackOperadores.append(p[-1])

  @_('factor term2', 'factor term2 MULT term1 term',
     'factor term2 DIV term1 term')
  def term(self, p):
    if(hasattr(p,'term1')):
      print('term', p.term2)
      return p.term2
    else:
      return p.term2

  @_('')
  def term1(self, p):
    self.stackOperadores.append(p[-1])
    #print(p[-1])

  @_('')
  def term2(self, p):
    #print('aaaaaaa', p[-1])
    if (len(self.stackOperadores) == 0):
      return p[-1]
    operadorTop = self.stackOperadores[-1]
    if (operadorTop == '*' or operadorTop == '/'):
      return self.genQuad()
    return p[-1]

  @_('ID fact1 arr', 'ID fact1 LPAREN logic multiexp RPAREN', 'CTE_NUM ctes1',
     'CTE_FLT ctes2', 'CTE_STR ctes3', 'TRUE ctes4', 'FALSE ctes4')
  def factor(self, p):
    return p[0]

  @_('')
  def ctes1(self, p):
    added = self.cteDir.add_cte(p[-1], self.intcte, 'int')
    if added:
      self.stackOperandos.append(self.intcte)
      self.intcte += 1
    else:
      addr = self.cteDir.get_entry(p[-1]).addr
      self.stackOperandos.append(addr)
      # address = dicrectorioconstantes.get entry(p[-1]).addr
    self.stackTypes.append('int')
    return p[-1]

  @_('')
  def ctes2(self, p):
    added = self.cteDir.add_cte(p[-1], self.fltcte, 'float')
    if added:
      self.stackOperandos.append(self.fltcte)
      self.fltcte += 1
    else:
      addr = self.cteDir.get_entry(p[-1]).addr
      self.stackOperandos.append(addr)
    self.stackTypes.append('float')
    return p[-1]

  @_('')
  def ctes3(self, p):
    added = self.cteDir.add_cte(p[-1], self.charcte, 'char')
    if added:
      self.stackOperandos.append(self.charcte)
      self.charcte += 1
    else:
      addr = self.cteDir.get_entry(p[-1]).addr
      self.stackOperandos.append(addr)
    self.stackTypes.append('char')
    return p[-1]

  @_('')
  def ctes4(self, p):
    added = self.cteDir.add_cte(p[-1], self.boolcte, 'bool')
    if added:
      self.stackOperandos.append(self.boolcte)
      self.boolcte += 1
    else:
      addr = self.cteDir.get_entry(p[-1]).addr
      self.stackOperandos.append(addr)
    self.stackTypes.append('bool')
    return p[-1]

  @_('')
  def fact1(self, p):
    aux = self.checkVarExists(p[-1])
    self.stackOperandos.append(aux.get_addr())
    self.stackTypes.append(aux.get_type())

  @_('COMMA logic multiexp', 'empty')
  def multiexp(self, p):
    pass

  @_('IF LPAREN logic if1 RPAREN stmnt else_stmnt END if2')
  def if_stmnt(self, p):
    pass

  @_('')
  def if1(self, p):
    exp_type = self.stackTypes.pop()
    if (exp_type != 'bool'):
      raise Exception("ERROR - Not a boolean expression")
    else:
      result = self.stackOperandos.pop()
      self.quadList.append(Quadruple(result, '', 'GOTOF', ''))
      self.stackJumps.append(self.quadCont)
      self.quadCont += 1

  @_('')
  def if2(self, p):
    end = self.stackJumps.pop()
    self.quadList[end - 1].res = self.quadCont

  @_('ELSE else1 stmnt', 'empty')
  def else_stmnt(self, p):
    pass

  @_('')
  def else1(self, p):
    self.quadList.append(Quadruple('', '', 'GOTO', ''))
    falso = self.stackJumps.pop()
    self.stackJumps.append(self.quadCont)
    self.quadCont += 1
    self.quadList[falso - 1].res = self.quadCont

  @_('WHILE while1 LPAREN logic while2 RPAREN stmnt while3 END')
  def while_stmnt(self, p):
    pass

  @_('')
  def while1(self, p):
    self.stackJumps.append(self.quadCont)

  @_('')
  def while2(self, p):
    exp_type = self.stackTypes.pop()
    if (exp_type != 'bool'):
      raise Exception("ERROR - Not a boolean expression")
    else:
      result = self.stackOperandos.pop()
      self.quadList.append(Quadruple(result, '', 'GOTOF', ''))
      self.stackJumps.append(self.quadCont)
      self.quadCont += 1

  @_('')
  def while3(self, p):
    end = self.stackJumps.pop()
    retorno = self.stackJumps.pop()
    self.quadList.append(Quadruple(retorno, '', 'GOTO', ''))
    self.quadCont += 1
    self.quadList[end - 1].res = self.quadCont

  @_('')
  def empty(self, p):
    pass

  # def error(self, p):
  #   print("Whoa. You are seriously hosed.")
  #   if not p:
  #     print("End of File!")
  #     return
  #   print(p)


if __name__ == '__main__':
  lexer = EmilLexer()
  parser = EmilParser()
  filename = 'tests/test.txt'

  if (len(sys.argv) > 1):
    filename = sys.argv[1]

  with open(filename) as fp:
    try:
      result = parser.parse(lexer.tokenize(fp.read()))
      print(result)
    except EOFError:
      pass
    except Exception as err:
      print(err)
