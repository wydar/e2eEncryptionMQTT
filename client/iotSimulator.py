from parser import parse_command
from security import handShake

args = parse_command()

print('##############################')
print('--- IoT Device Simulator ----')
print('--- Input\t::\t' + str(args.input))
print('--- Output\t::\t' + str(args.output))
print('##############################')
print('\nTry -h --help for more information\n')

handShake()


