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
            #print('address', address, self.ints)
            return int(self.ints[address])
        elif address < 2000:
            return self.floats[address % 1000]
        elif address < 3000:
            return self.chars[address % 1000]
        else:
            return self.bools[address % 1000]

    def set_value_in_address(self, address, value):
        if address < 1000:
            self.ints[address] = value
        elif address < 2000:
            self.floats[address % 1000] = value
        elif address < 3000:
            print('chars', self.chars, address, value)
            self.chars[address % 1000] = value
        else:
            self.bools[address % 1000] = value

    def set_param_value_in_address(self, value, type):
        if type == 'int':
            idx = next(idx for idx, item in enumerate(
                self.ints) if item is None)
            self.ints[idx] = value
        elif type == 'float':
            idx = next(idx for idx, item in enumerate(
                self.floats) if item is None)
            self.floats[idx] = value
        elif type == 'char':
            idx = next(idx for idx, item in enumerate(
                self.chars) if item is None)
            self.chars[idx] = value
        else:
            idx = next(idx for idx, item in enumerate(
                self.bools) if item is None)
            self.bools[idx] = value


def init_cte_mem(file):
    _, *values = file.readline().rstrip().split('~')
    ints = values
    _, *values = file.readline().rstrip().split('~')
    floats = values
    _, *values = file.readline().rstrip().split('~')
    chars = values
    _, *values = file.readline().rstrip().split('~')
    bools = values
    constants_mem = Memory(len(ints), len(
        floats), len(chars), len(bools))
    if (ints[0] != ''):
        constants_mem.insert_ints(ints)
    if (floats[0] != ''):
        constants_mem.insert_floats(floats)
    if (chars[0] != ''):
        constants_mem.insert_chars(chars)
    if (bools[0] != ''):
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
aux_local = None
aux_temp = None
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

#get value of left operand
def get_values(operando):
    bloques_mem = {
    '0' : local_mem,
    '1' : global_mem,
    '2' : temp_mem,
    '3' : cte_mem
    }
    
    bloquelo, addrlo = divmod(int(operando), 4000)
    #print(operando, bloquelo, bloques_mem[str(bloquelo)])
    return bloques_mem[str(bloquelo)].get_value_of_address(addrlo)

    #get result addr

def set_val(res, z):
    bloques_mem = {
    '0' : local_mem,
    '1' : global_mem,
    '2' : temp_mem,
    '3' : cte_mem
    }

    bloque, addr = divmod(int(res), 4000)
    return bloques_mem[str(bloque)].set_value_in_address(addr, z) 

def do_sum(lo,ro,res):
    x = get_values(lo)
    y = get_values(ro)

    set_val(res, x+y)

def do_sub(lo,ro,res):
    x = get_values(lo)
    y = get_values(ro)

    set_val(res, x-y)

def do_mult(lo,ro,res):
    x = get_values(lo)
    y = get_values(ro)

    set_val(res, x*y)

def do_div(lo,ro,res):
    x = get_values(lo)
    y = get_values(ro)

    set_val(res, x/y)

def less_than(lo,ro,res):
    x = get_values(lo)
    y = get_values(ro)

    set_val(res, x<y)

def more_than(lo,ro,res):
    x = get_values(lo)
    y = get_values(ro)

    set_val(res, x>y)

def less_eq_than(lo,ro,res):
    x = get_values(lo)
    y = get_values(ro)

    set_val(res, x<=y)

def more_eq_than(lo,ro,res):
    x = get_values(lo)
    y = get_values(ro)

    set_val(res, x>=y)

def is_eq(lo,ro,res):
    x = get_values(lo)
    y = get_values(ro)

    set_val(res, x==y)

def is_not_eq(lo,ro,res):
    x = get_values(lo)
    y = get_values(ro)

    set_val(res, x!=y)

def do_and(lo,ro,res):
    x = get_values(lo)
    y = get_values(ro)

    set_val(res, x and y)

def do_or(lo,ro,res):
    x = get_values(lo)
    y = get_values(ro)

    set_val(res, x or y)

def do_ass(lo,ro,res):
    #lo direccion a asignar
    #ro valor
    a = get_values(ro)

    set_val(lo,a)
    return

def do_goto(lo,ro,res):
    global instptr
    instptr = int(res) - 1

def do_gotof(lo,ro,res):
    global instptr
    result = get_values(lo)

    if(result == False):
        instptr = int(res) - 1
    return

def do_param(lo,ro,res):
    tipo = param_vars[funcname][int(ro)]
    value = get_values(res)

    aux_local.set_param_value_in_address(value, tipo)
    return

def do_era(lo,ro,res):
    global aux_local, aux_temp, funcname

    funcname = lo
    
    aux_local = Memory(lcl_vars[lo][0], lcl_vars[lo][1], lcl_vars[lo][2], lcl_vars[lo][3])
    aux_temp =  Memory(temp_vars[lo][0], temp_vars[lo][1], temp_vars[lo][2], temp_vars[lo][3])
    return

def do_gosub(lo,ro,res):
    global local_mem, temp_mem, instptr
    local_stack.append(local_mem)
    temp_stack.append(temp_mem)
    
    local_mem = aux_local
    temp_mem = aux_temp
    
    ptr_stack.append(instptr)
    instptr = int(res) - 1
    return

def do_return(lo, ro, res):
    global local_mem, temp_mem, instptr
    parche = get_values(res)
    
    local_mem = local_stack.pop()
    temp_mem = temp_stack.pop()
    instptr = ptr_stack.pop()

    return

def do_endfunc(lo,ro,res):
    global local_mem, temp_mem, instptr
    local_mem = local_stack.pop()
    temp_mem = temp_stack.pop()
    instptr = ptr_stack.pop()
    return

def do_write(lo,ro,res):
    sys.stdout.write(get_values(res))
    return

def do_read(lo,ro,res):
    x = sys.stdin.readline().rstrip()
    
    set_val(res, x)

def do_endprog(lo,ro,res):
    exit(0)

def init_temp_mem(funcname):
    ints, flts, chars, bools = temp_vars[funcname]
    return Memory(int(ints), int(flts), int(chars), int(bools))

lcl_vars = {}
temp_vars = {}
param_vars = {}
func_addr = {}
local_stack = []
temp_stack = []
ptr_stack = []
currFunc = None

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
    'READ': do_read,
    'WRITE': do_write,
    'and': do_and,
    'or': do_or,
    'GOTO': do_goto,
    'GOTOF': do_gotof,
    'PARAMETER': do_param,
    'ERA': do_era,
    'GOSUB': do_gosub,
    'RETURN' :do_return,
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
            func_addr[funcname] = int(values[0])
            lcl_vars[funcname] = [int(val) for val in values[1:5]]
            temp_vars[funcname] = [int(val) for val in values[5:9]]
            param_vars[funcname] = values[9:]

            if(funcname == 'main'):
                break
        quads = file.readlines()

        temp_mem = init_temp_mem('main')

        while(instptr < len(quads)):
            op, lo, ro, res = quads[instptr].rstrip('\n').split(' ')
            print(op, lo, ro, res)
            operations[op](lo,ro,res) 

            instptr += 1
    