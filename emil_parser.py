from sly import Parser
from sly.yacc import _decorator as _
from emil_lexer import EmilLexer
import sys

class EmilParser(Parser):
    tokens = EmilLexer.tokens

    @_('PROGRAM ID SEMICLN varsdecl funcdecl main')
    def program(self, p):
        return 0
    
    @_('VARS multivd multid')
    def varsdecl(self, p):
        return 0

    @_('tipo COLON ID arr multid SEMICLN multivd', 'empty')
    def multivd(self, p):
        return 0

    @_('COMMA ID arr multid', 'empty')
    def multid(self, p):
        return 0
    
    @_('INT', 'FLOAT', 'CHAR')
    def tipo(self, p):
        return p[0]
    
    @_('LSQUARE exp RSQUARE', 'empty')
    def arr(self, p):
        return 0
    
    @_('FUNC tipofunc ID LPAREN param RPAREN varsdecl LCURLY stmnt RCURLY')
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
    
    @_('MAIN LPAREN RPAREN')
    def main(self, p):
        return 0
    
    @_('ass_stmnt', 'func_stmnt', 'ret_stmnt', 'read_stmnt', 'write_stmnt')
    def stmnt(self, p):
        return 0
    
    @_('ID arr ASS exp SEMICLN', 'ID arr ASS func_stmnt SEMICLN')
    def ass_stmnt(self, p):
        return 0
    
    @_('ID LPAREN arg RPAREN SEMICLN')
    def func_stmnt(self, p):
        return 0
    
    @_('exp multiarg', 'empty')
    def arg(self, p):
        return 0
    
    @_('COMMA arg multiarg', 'empty')
    def multiarg(self, p):
        return 0
    
    @_('RETURN LPAREN exp RPAREN SEMICLN')
    def ret_stmnt(self, p):
        return 0
    
    @_('READ LPAREN ID multid RPAREN SEMICLN')
    def read_stmnt(self, p):
        return 0
    
    @_('WRITE LPAREN ID multid RPAREN SEMICLN')
    def write_stmnt(self, p):
        return 0
    
    @_('term', 'term SUM exp', 'term SUB exp')
    def exp(self, p):
        pass

    @_('factor', 'factor MULT term', 'factor DIV term')
    def term(self, p):
        pass

    @_('ID arr', 'ID LPAREN exp multiexp RPAREN', 'CTE_NUM', 'CTE_FLT', 'CTE_STR')
    def factor(self, p):
        pass

    @_('COMMA exp multiexp', 'empty')
    def multiexp(self, p):
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

    # with open(filename) as fp:
    #     try:
    #         result = parser.parse(lexer.tokenize(fp.read()))
    #         print(result)
    #     except EOFError:
    #         pass
    #     except Exception as err:
    #         print(err)