JavaScript Object Notation
==========================

.. py:currentmodule:: textform.formats.json

The ``json`` format uses the :py:mod:`json` module to read and write records using an interface
that looks like :py:mod:`csv`.

The difference between strict JSON and line-oriented json (:py:mod:`textform.formats.jsonl`)
is that strict JSON writes out all the records on one line as a JSON array.

.. py:class:: LineReader(iterable, **config)

    This is simply an alias for :py:class:`textform.jsonl.LineReader`.

.. py:class:: DictReader()

    This is simply an alias for :py:class:`textform.jsonl.DictReader`.

.. py:class:: LineWriter(outfile, fieldnames, **config)

    This is simply an alias for :py:class:`textform.jsonl.LineWriter`.

.. py:class:: DictWriter(outfile, fieldnames, **config)

    A :py:class:`textform.formats.DictWriter` that

    .. py:method:: writeheader()

        Writes an initial ``[``.

    .. py:method:: writerow(row)

        Writes the row in JSON format with a comma separator if necessary.

    .. py:method:: writefooter()

        Writes a terminating ``]``.


