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

    #print(constants_mem.ints, constants_mem.floats, constants_mem.chars, constants_mem.bools)
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

    print(len(global_mem.ints), len(global_mem.floats), len(global_mem.chars), len(global_mem.bools))
    return global_mem

# operations = {
#     '+': do_sum,
#     '-': do_sub,
#     '*': do_mult,
#     '/': do_div,
#     '<': less_than,
#     '>': more_than,
#     '<=': less_eq_than,
#     '>=': more_eq_than,
#     '==': is_eq,
#     '<>': is_not_eq,
#     '=': do_ass,
#     'GOTO': do_goto,
#     'GOTOF': do_gotof,
#     'PARAM': do_param,
#     'ERA': do_era,
#     'GOSUB': do_gosub,
#     'ENDFUNC': do_endfunc,
#     'ENDPROG': do_endprog
# }

if __name__ == '__main__':
    filename = sys.argv[1]
    instptr = 0

    with open(filename) as file:
        init_cte_mem(file)
        init_glb_mem(file)
        quads = file.readlines()
        
        print((quads))