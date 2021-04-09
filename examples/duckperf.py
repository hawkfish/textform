import csv
import re
import sys

sys.path.append('..')
from textform import *

def main():
    p = Text(sys.stdin, 'Line')
    p = Add(p, 'Branch', sys.argv[1])
    p = Match(p, 'Line', '-', True)
    p = Divide(p, 'Line', 'Query', 'Run', 'Q')
    p = Fill(p, 'Query', '00')
    p = Capture(p, 'Query', ('Query',), r'\|\|\s+Q(\w+)\s+\|\|')
    p = Split(p, 'Query', ('Query', 'Mode',), '_', ('00', 'SERIAL',))
    p = Cast(p, 'Query', int)
    p = Match(p, 'Run', r'\d')
    p = Capture(p, 'Run', ('Run #', 'Run Count', 'Time',), r'(\d+)/(\d+)...(\d+\.\d+)')
    p = Cast(p, 'Run #', int)
    p = Cast(p, 'Run Count', int)
    p = Cast(p, 'Time', float)
    p = Write(p, sys.stdout)
    print(p.pull(), file=sys.stderr)

if __name__ == '__main__':
    main()
