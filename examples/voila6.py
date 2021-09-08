import os.path
import sys

sys.path.append(os.path.join('..', 'src'))
from textform import *

def main():
    p = Text(open('voila6.txt', 'r'), 'Value')
    # Convert the ragged values to a single column
    fmt = {'delimiter': ' '}
    p = Iterate(p, 'Value', 'Index', 'Value', layout='csv', **fmt)
    p = Drop(p, 'Index')
    # Split apart the 1-2 digit fused values
    p = Replace(p, 'Value', r'^([567])(\d{1,2})$', r'\1 \2')
    p = Iterate(p, 'Value', 'Index', 'Value', layout='csv', **fmt)
    p = Drop(p, 'Index')
    # Get rid of the Runtime line
    p = Match(p, 'Value', r'Runtime|\(', True)
    # Clean up the Quantile labels
    p = Replace(p, 'Value', r'^Q0.(\d+)', r'Q\1')
    # Use the Median label to mark the changeover from interleaved data to single columns
    p = Copy(p, 'Value', 'Copy')
    p = Divide(p, 'Copy', 'Columns', 'Data', r'Median')
    p = Drop(p, 'Data')
    p = Replace(p, 'Columns', 'Median', '1')
    p = Fill(p, 'Columns', '2')
    p = Cast(p, 'Columns', int)
    # Compute the row number of the values within the interleaving
    p = Sequence(p, 'Row', 0)
    p = Project(p, ('Row', 'Columns',), 'Index', lambda r, c: r % c)
    p = Project(p, ('Row', 'Index',), 'Fixed', lambda r, i: r-i)
    p = Drop(p, ('Row', 'Columns',))
    # Unfold the ragged interleaved columns
    p = Unfold(p, ('Index', 'Value',), ('Left', 'Right',))
    p = Drop(p, 'Fixed')
    # Unfold the 8 values in each column into values after that column name
    p = Sequence(p, 'Row', 0)
    p = Project(p, ('Row',), 'Tags', lambda r: r % 8)
    p = Drop(p, 'Row')
    # Unfold the interleaved columns into two fused rows
    lefts = ['L%d' % i for i in range(8)]
    rights = ['R%d' % i for i in range(8)]
    unfolded = lefts + rights
    p = Unfold(p, ('Tags', 'Left', 'Right',), unfolded)
    # Fold the fused row into two unfused rows
    p = Fold(p, unfolded, ['Tags', 'Data',])
    p = Drop(p, 'Tags')
    # Remove the None values from the ragged folding
    p = Select(p, 'Data', lambda v: v is not None)
    # Unfold the rows into a single 7x8 block using row and column numbering
    p = Sequence(p, 'Index', 0)
    p = Project(p, ('Index',), 'Row', lambda r: r % 8)
    p = Project(p, ('Index',), 'Column', lambda r: r // 8)
    p = Drop(p, 'Index')
    unfolded = ('#BLENDs', '#Queries', 'Min', 'Q25', 'Median', 'Q75', 'Max',)
    offsets = {i: i for i in range(len(unfolded))}
    p = Unfold(p, ('Column', 'Data',), unfolded, offsets)
    p = Drop(p, 'Row')
    # Get rid of the redundant column headers
    p = Match(p, '#BLENDs', '#BLENDs', True)
    # Cast the numeric values
    p = Cast(p, '#Queries', int)
    p = Cast(p, 'Min', float)
    p = Cast(p, 'Q25', float)
    p = Cast(p, 'Median', float)
    p = Cast(p, 'Q75', float)
    p = Cast(p, 'Max', float)
    # Export the csv
    p = Write(p, sys.stdout)
    print(p.pump(), file=sys.stderr)

if __name__ == '__main__':
    main()
