# textform

A data transformation pipeline module based on the seminal [Potter's Wheel](http://control.cs.berkeley.edu/pwheel-vldb.pdf) data wrangling formalism. The name is a portmanteau of "text" and "transform".

## Overview

`textform` (abbreviated `txf`) is a text-oriented data transformation module. With it, you can create sequential record processing _pipelines_ that convert data from (say) lines of text into records and then route the final record stream for another use (e.g, write the records to a `csv` file.)

Pipelines are cosntructed from a sequence of _transforms_ that take in a record and modify it in some way. For example, the `Split` transform will replace an input field with several new fields that are derived from the input by splitting on a pattern.

While inspired by the Potter's Wheel transform list, `textform` is designed for practical everyday use. This means it includes transforms for limiting the number of rows, writing intermediate results to files and capturing via regular expressions.

## Audience

How do I know if `textform` is right for me? The simplest use case is where you want to use Python's `DictReader` but the file isn't a `csv`. With `textform` you can write a pipeline that will end up producing the records you would get from `DictReader`.

More complex use cases can be built on top of this kind of record stream. Reshaping, computing values, splitting, dividing, merging, filling in blanks and other kinds of data cleaning and preparation tasks can all be implemented in a reusable fashion with `textform`. A pipeline effectively describes the format of a text file in an executable fashion that can be reused.

## Example

I created `textform` because I had worked on [a similar research system](https://tc19.tableau.com/learn/sessions/lets-get-physical-preparing-data-text-files) in the past and had two text files produced by the [DuckDB](https://github.com/duckdb/duckdb) performance test suite that I needed to convert into `csv`s:

```
------------------
|| Q01_PARALLEL ||
------------------
Cold Run...Done!
Run 1/5...0.12345
Run 1/5...0.12345
Run 1/5...0.12345
Run 1/5...0.12345
Run 1/5...0.12345
------------------
|| Q02_PARALLEL ||
------------------
...
```

This file is esssentially a sequence of records grouped by higher attributes. Instead of writing a one-off Python script, I decided to write some simple transforms and build a pipeline, which looked like this:

```py
p = Text(sys.stdin, 'Line')                         # Read a line
p = Add(p, 'Branch', sys.argv[1])                   # Tag the file with the branch name
p = Match(p, 'Line', r'------', invert=True).       # Remove horizontal lines
p = Divide(p, 'Line', 'Query', 'Run', r'Q')         # Separate the query names from the run data
p = Fill(p, 'Query', '00')                          # Fill down the blank query names
p = Capture(p, 'Query', ('Query',), r'\|\|\s+Q(\w+)\s+\|\|')  # Capture the query number
# Split the execution mode from the query name
p = Split(p, 'Query', ('Query', 'Mode',), r'_', ('00', 'SERIAL',))
p = Cast(p, 'Query', int)                           # Cast the query number to an integer
p = Match(p, 'Run', r'\d')                          # Filter to the runs with data
# Capture the run components
p = Capture(p, 'Run', ('Run #', 'Run Count', 'Time',), r'(\d+)/(\d+)...(\d+\.\d+)')
p = Cast(p, 'Run #', int)                           # Cast the run components
p = Cast(p, 'Run Count', int)
p = Cast(p, 'Time', float)
p = Write(p, sys.stdout)                            # Write the records to stdout as a csv
p.pump()
```

We can now invoke the pipeline script as:

```shell
$ python3 pipeline.py master < performance.txt > performance.csv
```

## Contributing

You know the drill: Fork, branch, test submit a PR.  This is a completely open source, free as in beer project.
