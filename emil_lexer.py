from sly import Lexer
from sly.yacc import _decorator as _
import sys
import re


class EmilLexer(Lexer):
  tokens = {
      ID, CTE_NUM, CTE_FLT, CTE_STR, SEMICLN, COLON, COMMA, ASS, SUM, SUB,
      MULT, DIV, EQUAL_TO, LESS_THAN, MORE_THAN, LESS_OR_EQ_THAN,
      MORE_OR_EQ_THAN, DIFFERENT_TO, LSQUARE, RSQUARE, LPAREN, RPAREN, LCURLY,
      RCURLY, MAIN, PROGRAM, VARS, INT, CHAR, FLOAT, BOOL, READ, WRITE, IF,
      ELSE, WHILE, END, TRUE, FALSE, AND, OR, FUNC, VOID, RETURN
  }

  # reserved_words = ['program', 'vars', 'int', 'char', 'float', 'bool', 'read', 'write', 'if', 'else', 'while', 'func', 'true', 'false', 'and', 'or', 'end', 'void', 'main', 'return']

  ignore = ' \t'
  ignore_comment = r'#.*'

  CTE_FLT = r'-?\d+\.\d+'
  CTE_NUM = r'-?\d+'
  CTE_STR = r'\"[^\"\n]*\"'
  ID = r'[a-z][a-z0-9_]*'
  SEMICLN = r'\;'
  COLON = r'\:'
  SUM = r'\+'
  SUB = r'\-'
  MULT = r'\*'
  DIV = r'\/'
  EQUAL_TO = r'=='
  LESS_OR_EQ_THAN = r'<='
  MORE_OR_EQ_THAN = r'>='
  ASS = r'='
  DIFFERENT_TO = r'<>'
  LESS_THAN = r'<'
  MORE_THAN = r'>'
  COMMA = r','
  LPAREN = r'\('
  RPAREN = r'\)'
  LSQUARE = r'\['
  RSQUARE = r'\]'
  LCURLY = r'\{'
  RCURLY = r'\}'
  VARS = r'VARS'

  ID['main'] = MAIN
  ID['program'] = PROGRAM
  #ID['VARS'] = VARS
  ID['int'] = INT
  ID['char'] = CHAR
  ID['float'] = FLOAT
  ID['bool'] = BOOL
  ID['read'] = READ
  ID['write'] = WRITE
  ID['if'] = IF
  ID['else'] = ELSE
  ID['while'] = WHILE
  ID['func'] = FUNC
  ID['true'] = TRUE
  ID['false'] = FALSE
  ID['and'] = AND
  ID['or'] = OR
  ID['end'] = END
  ID['void'] = VOID
  ID['return'] = RETURN

  @_(r'\n+')
  def ignore_newline(self, t):
    self.lineno += len(t.value)

  def error(self, t):
    print("ERROR: Illegal character '%s' found" % t.value[0])
    self.index += 1
