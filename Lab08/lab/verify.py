import subprocess

output = subprocess.getoutput('cat solve_input | ./src/prog')

print(output)
if output[-3:] == 'AC!':
    print('Verify: AC')
    exit(0)
else :
    print('Verify: WA')
    exit(1)
