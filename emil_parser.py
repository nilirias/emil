from sly import Parser
from sly.yacc import _decorator as _
from emil_lexer import EmilLexer
from quads import Quadruple
import sys

class EmilParser(Parser):
    tokens = EmilLexer.tokens
    quadList = []
    stackOperadores = []
    stackOperandos = []
    tempCont = 0

    @_('PROGRAM ID SEMICLN varsdecl funcdecl main')
    def program(self, p):
        for quad in self.quadList:
            print(quad)
        return 69
    
    @_('VARS multivd multid', 'empty')
    def varsdecl(self, p):
        return 0

    @_('tipo COLON ID arr multid SEMICLN multivd', 'empty')
    def multivd(self, p):
        return 0

    @_('COMMA ID arr multid', 'empty')
    def multid(self, p):
        return 0
    
    @_('INT', 'FLOAT', 'CHAR', 'BOOL')
    def tipo(self, p):
        return p[0]
    
    @_('LSQUARE exp RSQUARE', 'empty')
    def arr(self, p):
        return 0
    
    @_('FUNC tipofunc ID LPAREN param RPAREN varsdecl LCURLY stmnt RCURLY', 'empty')
    def funcdecl(self, p):
        return 0
    
    @_('VOID', 'tipo')
    def tipofunc(self, p):
        return p[0]
    
    @_('tipo COLON ID multiparam', 'empty')
    def param(self, p):
        return 0
    
    @_('COMMA param', 'empty')
    def multiparam(self, p):
        return 0
    
    @_('MAIN LPAREN RPAREN stmnt')
    def main(self, p):
        return 0
    
    @_('ass_stmnt stmnt', 'func_stmnt stmnt', 'ret_stmnt stmnt', 'read_stmnt stmnt', 'write_stmnt stmnt', 'if_stmnt stmnt', 'while_stmnt stmnt', 'empty')
    def stmnt(self, p):
        return 0
    
    @_('ID arr ASS logic SEMICLN', 'ID arr ASS func_stmnt SEMICLN')
    def ass_stmnt(self, p):
        return 0
    
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
    
    @_('READ LPAREN ID multid RPAREN SEMICLN')
    def read_stmnt(self, p):
        return 0
    
    @_('WRITE LPAREN ID multid RPAREN SEMICLN')
    def write_stmnt(self, p):
        return 0
    
    @_('rel', 'rel AND logic', 'rel OR logic')
    def logic(self, p):
        pass
    
    @_('MORE_THAN', 'LESS_THAN', 'MORE_OR_EQ_THAN', 'LESS_OR_EQ_THAN', 'DIFFERENT_TO', 'EQUAL_TO')
    def relop(self, p):
        pass
    
    @_('exp', 'exp relop exp')
    def rel(self, p):
        pass

    @_('term exp2', 'term exp2 SUM exp1 exp', 'term exp2 SUB exp1 exp')
    def exp(self, p):
        pass

    @_('')
    def exp2(self, p):
        if(len(self.stackOperadores) == 0):
            return
        operadorTop = self.stackOperadores[-1]
        if(operadorTop == '+' or operadorTop == '-'):
            print(self.stackOperandos)
            rightOp = self.stackOperandos.pop()
            leftOp = self.stackOperandos.pop()
            op = self.stackOperadores.pop()
            self.quadList.append(Quadruple(leftOp, rightOp, op, f't{self.tempCont}'))

            self.stackOperandos.append(f't{self.tempCont}')
            self.tempCont += 1

    @_('')
    def exp1(self, p):
        self.stackOperadores.append(p[-1])
        #print(p[-1])

    @_('factor term2', 'factor term2 MULT term1 term', 'factor term2 DIV term1 term')
    def term(self, p):
        pass

    @_('')
    def term1(self, p):
        self.stackOperadores.append(p[-1])

    @_('')
    def term2(self, p):
        if(len(self.stackOperadores) == 0):
            return
        operadorTop = self.stackOperadores[-1]
        if(operadorTop == '*' or operadorTop == '/'):
            print(self.stackOperandos)
            rightOp = self.stackOperandos.pop()
            leftOp = self.stackOperandos.pop()
            op = self.stackOperadores.pop()
            self.quadList.append(Quadruple(leftOp, rightOp, op, f't{self.tempCont}'))

            self.stackOperandos.append(f't{self.tempCont}')
            self.tempCont += 1

    @_('ID fact1 arr', 'ID fact1 LPAREN logic multiexp RPAREN', 'CTE_NUM fact1', 'CTE_FLT fact1', 'CTE_STR fact1', 'TRUE fact1', 'FALSE fact1')
    def factor(self, p):
        pass

    @_('')
    def fact1(self, p):
        self.stackOperandos.append(p[-1])

    @_('COMMA logic multiexp', 'empty')
    def multiexp(self, p):
        pass

    @_('IF LPAREN logic RPAREN else_stmnt END')
    def if_stmnt(self, p):
        pass

    @_('ELSE stmnt', 'empty')
    def else_stmnt(self, p): 
        pass

    @_('WHILE LPAREN logic RPAREN stmnt END')
    def while_stmnt(self, p):
        pass

    @_('')
    def empty(self, p):
        pass
    
if __name__ == '__main__':
    lexer = EmilLexer()
    parser = EmilParser()
    filename = 'tests/test.txt'

    if(len(sys.argv) > 1):
        filename = sys.argv[1]

    with open(filename) as fp:
        try:
            result = parser.parse(lexer.tokenize(fp.read()))
            print(result)
        except EOFError:
            pass
        except Exception as err:
            print(err)