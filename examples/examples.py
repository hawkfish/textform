import os.path
import sys

sys.path.append(os.path.join('..', 'src'))
from textform import *

def f(s):
    return open(f"{s}_example.csv", "w")

def main():
    p = Text(open('duckperf.txt', 'r'), 'Line')
    p = Limit(p, 10)
    p = Write(p, f('limit'), 'rst')
    p = Match(p, 'Line', '-', True)
    p = Write(p, f('match'), 'rst')
    p = Add(p, 'Branch', 'master')
    p = Write(p, f('add'), 'rst')
    p = Divide(p, 'Line', 'Query', 'Run', 'Q')
    p = Write(p, f('divide'), 'rst')
    p = Fill(p, 'Query', 'Q00')
    p = Write(p, f('fill'), 'rst')
    p = Capture(p, 'Query', ('Query',), r'\|\|\s+Q(\w+)\s+\|\|')
    p = Write(p, f('split_in'), 'rst')
    p = Split(p, 'Query', ('Query', 'Mode',), '_', ('00', 'SERIAL',))
    p = Write(p, f('split'), 'rst')
    p = Cast(p, 'Query', int)
    p = Write(p, f('cast'))
    p = Match(p, 'Run', r'\d')
    p = Write(p, f('capture_in'), 'rst')
    p = Capture(p, 'Run', ('Run #', 'Run Count', 'Time',), r'(\d+)/(\d+)...(\d+\.\d+)')
    p = Write(p, f('capture'), 'rst')
    p = Cast(p, 'Run #', int)
    p = Cast(p, 'Run Count', int)
    p = Cast(p, 'Time', float)
    print(p.pump(), file=sys.stderr)

if __name__ == '__main__':
    main()
