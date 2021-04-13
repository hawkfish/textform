import argparse
import os.path
import sys

sys.path.append(os.path.join('..', 'src'))
from textform import *

def informat_arg_type(format):
    if format not in ('csv', 'json', 'jsonl', 'md', 'text',):
        raise argparse.ArgumentTypeError(f"Argument '{format}' is not an input format.")

    return format

def outformat_arg_type(format):
    if format not in ('csv', 'json', 'jsonl', 'md',):
        raise argparse.ArgumentTypeError(f"Argument '{format}' is not an output format.")

    return format

def main():
    parser = argparse.ArgumentParser(description="Convert a flat file from one fromat to another.")
    parser.add_argument("--in-format", "-i", type=informat_arg_type, default='csv',
                        help="The input format (default csv)")
    parser.add_argument("--out-format", "-o", type=outformat_arg_type, default='jsonl',
                        help="The output format (default jsonl)")
    config = parser.parse_args()

    p = Read(sys.stdin, None, config.in_format)
    p = Write(p, sys.stdout, config.out_format)
    print(p.pump(), file=sys.stderr)

if __name__ == '__main__':
    main()
