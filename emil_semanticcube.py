art_ops = ['+', '-', '/', '*']
rel_ops = ['<', '>', '<=', '>=']
log_ops = ['and', 'or']
eq_ops = ['<>', '==']

def checkArt(type1, type2, operator):
    if type1 == 'int' and type2 == 'int':
        return 'int'
    if type1 == 'int' and type2 == 'float':
        return 'float'
    if type1 == 'float' and type2 == 'int':
        return 'float'
    if type1 == 'float' and type2 == 'float':
        return 'float'

    if type1 == 'char' and type2 == 'char' and operator == '+':
        return 'char'
    if type1 == 'char' and type2 == 'int' and operator == '+':
      return 'char'
    raise TypeError(f'{operator} cannot operate between {type1} and {type2}')

def checkRel(type1, type2, operator):
  if type1 == 'int' and type2 == 'int':
    return 'bool'
  if type1 == 'int' and type2 == 'float':
    return 'bool'
  if type1 == 'float' and type2 == 'int':
    return 'bool'
  if type1 == 'int' and type2 == 'int':
    return 'bool'
  raise TypeError(f'{operator} cannot operate between {type1} and {type2}')

def checkLog(type1, type2, operator):
  if type1 == 'bool' and type2 == 'bool':
    return 'bool'
  if type1 == 'int' and type2 == 'int':
    return 'bool'
  if type1 == 'int' and type2 == 'float':
    return 'bool'
  if type1 == 'float' and type2 == 'float':
    return 'bool'
  if type1 == 'float' and type2 == 'int':
    return 'bool'

def checkEq(type1, type2, operator):
  if type1 == type2:
    return 'bool'

def checkAss(type1, type2, operator):
  if type1 == type2:
    return type1

def checkOperator(type1, type2, operator):
  if operator in art_ops:
    return checkArt(type1, type2, operator)
  if operator in rel_ops:
    return checkRel(type1, type2, operator)
  if operator in log_ops:
    return checkLog(type1, type2, operator)
  if operator in eq_ops:
    return checkEq(type1, type2, operator)
  if operator == '=':
    return checkAss(type1, type2, operator)
  raise Exception(f'Opertator {operator} not defined in specification')