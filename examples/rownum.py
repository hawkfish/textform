import os.path
import sys

sys.path.append(os.path.join('..', 'src'))
from textform import *

def main():
    p = Sequence(None, sys.argv[1], 1)
    p = Read(sys.stdin, p)
    p = Write(p, sys.stdout)
    print(p.pump(), file=sys.stderr)

if __name__ == '__main__':
    main()
