import angr
import sys # for stdin

EQUATION_CNT = 14
VARIABLE_CNT = 15

main_addr = 0x4011a9
find_addr = 0x401363
# find_addr = 0x401371
avoid_addr = 0x40134d

class my_scanf(angr.SimProcedure):
    def run(self,fmt,n): # 参数为 (self + 该函数实际参数)
        simfd = self.state.posix.get_fd(0) # stdin
        data,real_size = simfd.read_data(0x04) # 注意该函数返回两个值 第一个是读到的数据内容 第二个数内容长度
        self.state.memory.store(n,data) # 将数据保存到相应参数内
        return real_size # 返回原本函数该返回的东西

########################################################

proj = angr.Project('./src/prog', load_options={'auto_load_libs': False})
proj.hook_symbol('__isoc99_scanf', my_scanf(), replace=True)

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
        input = simgr.found[0].posix.dumps(sys.stdin.fileno())[i:i+4]
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