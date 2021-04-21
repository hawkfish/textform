JavaScript Object Notation
==========================

.. py:currentmodule:: txf.layouts.json

The ``json`` layout uses the :py:mod:`json` module to read and write records using an interface
that looks like :py:mod:`csv`.

The difference between strict JSON and line-oriented json (:py:mod:`txf.layouts.jsonl`)
is that strict JSON writes out all the records on one line as a JSON array.

.. py:class:: LineReader(iterable, **config)

    This is simply an alias for :py:class:`txf.jsonl.LineReader`.

.. py:class:: DictReader()

    This is simply an alias for :py:class:`txf.jsonl.DictReader`.

.. py:class:: LineWriter(outfile, fieldnames, **config)

    This is simply an alias for :py:class:`txf.jsonl.LineWriter`.

.. py:class:: DictWriter(outfile, fieldnames, **config)

    A :py:class:`txf.layouts.DictWriter` that

    .. py:method:: writeheader()

        Writes an initial ``[``.

    .. py:method:: writerow(row)

        Writes the row in JSON layout with a comma separator if necessary.

    .. py:method:: writefooter()

        Writes a terminating ``]``.


