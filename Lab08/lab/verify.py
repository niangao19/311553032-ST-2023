import subprocess

output = subprocess.getoutput('cat solve_input | ./src/prog')

print(output)
if output[-3:] == 'AC!':
    print('Verify: AC')
    exit(0)
elif output[-3:] == 'WA!':
    print('Verify: WA')
    exit(1)
else :
    print('no output')
    exit(1)