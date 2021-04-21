Comma Separated Values
======================

:py:mod:`textform` is designed to imitate the builtin :py:mod:`csv` module as closely as possible.
The readers for csv are therefore almost identical to those of the builtin module.

.. py:class:: LineReader()

    This is simply a wrapper for :py:class:`csv.reader`.

.. py:class:: DictReader()

    This is simply an alias for :py:class:`csv.DictReader`.

.. py:class:: LineWriter(outfile, fieldnames, **config)

    A subclass of :py:class:`csv.writer` that sets the ``lineterminator`` field to the empty string.

.. py:class:: DictWriter(outfile, fieldnames, **config)

    A subclass of :py:class:`csv.DictWriter` that sets the ``lineterminator`` field to newline.

    .. py:method:: writefooter()

        Writes the footer for CSV files, which is a NOP.


