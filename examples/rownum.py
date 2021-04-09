import csv
import re
import sys

sys.path.append('..')
from textform import *

def main():
    p = Sequence(None, sys.argv[1], 1)
    p = Read(sys.stdin, p)
    p = Write(p, sys.stdout)
    print(p.pull(), file=sys.stderr)

if __name__ == '__main__':
    main()
