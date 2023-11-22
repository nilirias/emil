import sys
import json

class Memory:
    def __init__(self, i, f, s, b):
        self.ints = [None] * int(i)
        self.floats = [None] * int(f)
        self.chars = [None] * int(s)
        self.bools = [None] * int(b)

    def insert_ints(self, arr_ints):
        for idx, values in enumerate(arr_ints):
            self.ints[idx] = int(values)

    def insert_floats(self, arr_floats):
        for idx, values in enumerate(arr_floats):
            self.floats[idx] = float(values)

    def insert_chars(self, arr_char):
        for idx, values in enumerate(arr_char):
            self.chars[idx] = values

    def insert_bools(self, arr_bools):
        for idx, values in enumerate(arr_bools):
            self.bools[idx] = values == 'true'

    def get_value_of_address(self, address):
        if address < 1000:
            return int(self.ints[address])
        elif address < 2000:
            return self.floats[address % 1000]
        elif address < 3000:
            return self.strings[address % 1000]
        else:
            return self.bools[address % 1000]

    def set_value_in_address(self, address, value):
        if address < 1000:
            self.ints[address] = value
        elif address < 2000:
            self.floats[address % 1000] = value
        elif address < 3000:
            self.strings[address % 1000] = value
        else:
            self.bools[address % 1000] = value


def init_cte_mem(file):
    _, *values = file.readline().rstrip('\n').split('~')
    ints = values
    _, *values = file.readline().rstrip('\n').split('~')
    floats = values
    _, *values = file.readline().rstrip('\n').split('~')
    chars = values
    _, *values = file.readline().rstrip('\n').split('~')
    bools = values
    constants_mem = Memory(len(ints), len(
        floats), len(chars), len(bools))
    constants_mem.insert_ints(ints)
    constants_mem.insert_floats(floats)
    constants_mem.insert_chars(chars)
    constants_mem.insert_bools(bools)

    return constants_mem

def init_glb_mem(file):
    _, values = file.readline().rstrip('\n').split('~')
    ints = values
    _, values = file.readline().rstrip('\n').split('~')
    floats = values
    _, values = file.readline().rstrip('\n').split('~')
    chars = values
    _, values = file.readline().rstrip('\n').split('~')
    bools = values
    global_mem = Memory(int(ints), int(
        floats), int(chars), int(bools))

    return global_mem

local_mem = None
global_mem = None
temp_mem = None
cte_mem = None
instptr = 0

bloques_mem = {}

# divmod 4000 pq cada bloque 4000 espacios
# 0 locales
# 1 g;obales
# 2 temporales
# 3 ctes
#
# luego
#
# divmod 1000 pq son 1000 espacios por tipo
# 0 int
# 1 flts
# 2 chars
# 3 bools
#

def do_sum(lo,ro,res):
    bloques_mem = {
    '0' : local_mem,
    '1' : global_mem,
    '2' : temp_mem,
    '3' : cte_mem
    }
    
    #get value of left operand
    bloquelo, addrlo = divmod(int(lo), 4000)
    print(lo, bloquelo, bloques_mem[str(bloquelo)])
    x = bloques_mem[str(bloquelo)].get_value_of_address(addrlo)

    #get value of right operand
    bloquero, addrro = divmod(int(ro), 4000)
    print(ro, bloquero, bloques_mem[str(bloquero)])
    y = bloques_mem[str(bloquero)].get_value_of_address(addrro)

    #get result addr
    bloqueres, addrres = divmod(int(res), 4000)
    z = x + y

    bloques_mem[str(bloqueres)].set_value_in_address(addrres, z) 

    print(x, y)
    return

def do_sub(lo,ro,res):
    return

def do_mult(lo,ro,res):
    return

def do_div(lo,ro,res):
    return

def less_than(lo,ro,res):
    return

def more_than(lo,ro,res):
    return

def less_eq_than(lo,ro,res):
    return

def more_eq_than(lo,ro,res):
    return

def is_eq(lo,ro,res):
    return

def is_not_eq(lo,ro,res):
    return

def do_ass(lo,ro,res):
    return

def do_goto(lo,ro,res):
    global instptr
    instptr = int(res) - 1

def do_gotof(lo,ro,res):
    return

def do_param(lo,ro,res):
    return

def do_era(lo,ro,res):
    global local_mem, temp_mem
    local_stack.append(local_mem)
    temp_stack.append(temp_mem)

    local_mem = Memory(lcl_vars[lo][0], lcl_vars[lo][1], lcl_vars[lo][2], lcl_vars[lo][3])
    temp_mem = Memory(temp_vars[lo][0], temp_vars[lo][1], temp_vars[lo][2], temp_vars[lo][3])
    return

def do_gosub(lo,ro,res):
    return

def do_endfunc(lo,ro,res):
    global local_mem, temp_mem
    local_mem = local_stack.pop()
    temp_mem = temp_stack.pop()
    return

def do_endprog(lo,ro,res):
    exit(0)

def init_temp_mem(funcname):
    ints, flts, chars, bools = temp_vars[funcname]
    return Memory(int(ints), int(flts), int(chars), int(bools))

lcl_vars = {}
temp_vars = {}
local_stack = []
temp_stack = []

operations = {
    '+': do_sum,
    '-': do_sub,
    '*': do_mult,
    '/': do_div,
    '<': less_than,
    '>': more_than,
    '<=': less_eq_than,
    '>=': more_eq_than,
    '==': is_eq,
    '<>': is_not_eq,
    '=': do_ass,
    'GOTO': do_goto,
    'GOTOF': do_gotof,
    'PARAMETER': do_param,
    'ERA': do_era,
    'GOSUB': do_gosub,
    'ENDFUNC': do_endfunc,
    'ENDPROG': do_endprog
}

if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename) as file:
        cte_mem = init_cte_mem(file)
        global_mem = init_glb_mem(file)

        while (True):
            funcname, *values = file.readline().rstrip('\n').split('~')
            lcl_vars[funcname] = [int(val) for val in values][0:4]
            temp_vars[funcname] =[int(val) for val in values][4:8]
            if(funcname == 'main'):
                break
        quads = file.readlines()

        temp_mem = init_temp_mem('main')

        while(instptr < len(quads)):
            op, lo, ro, res = quads[instptr].rstrip('\n').split(' ')
            print(op, lo, ro, res)
            operations[op](lo,ro,res) 

            instptr += 1
