import angr
import sys # for stdin

EQUATION_CNT = 14
VARIABLE_CNT = 15

main_addr = 0x4011a9
find_addr = 0x401371
# find_addr = 0x401371
avoid_addr = [0x40134d,0x40121a]

class my_scanf(angr.SimProcedure):
    def run(self,fmt,n): 
        simfd = self.state.posix.get_fd(sys.stdin.fileno())
        data,real_size = simfd.read_data(4) 
        self.state.memory.store(n,data) 
        return 1 



########################################################

proj = angr.Project('./src/prog', load_options={'auto_load_libs': False})
proj.hook_symbol('__isoc99_scanf', my_scanf(), replace=True)
proj.hook_symbol('printf', angr.SIM_PROCEDURES['stubs']['ReturnUnconstrained'](), replace=True)
state = proj.factory.blank_state(addr=main_addr)

simgr = proj.factory.simulation_manager(state)

simgr.explore(find=find_addr, avoid_addr=avoid_addr)

if simgr.found:
    print(simgr.found[0].posix.dumps(sys.stdin.fileno()))
    string_data = simgr.found[0].posix.dumps(sys.stdin.fileno())
    # 把字符串分成 14 段，每段长度为 4
    # num_strings = [string_data[i:i+4] for i in range(0, len(string_data), 4)]
    nums = []
    for i in range(0,len(string_data),4):
        input = string_data[i:i+4]
        input = int.from_bytes(input, byteorder='little', signed=True)
        print( f'x{int(i/4)} : {input}' )
        nums.append(input)
    # 把每段字符串转换成对应的整数
    # print(nums)
else :
    print('Failed')  

with open('solve_input', 'w') as f:
    for a in nums:
        f.write(f'{a}\n')
