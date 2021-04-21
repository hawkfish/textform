Google Markdown
===============

.. py:module:: txf.layouts.md

The ``md`` layout reads and writes records  as Markdown tables using an interface
that looks like :py:mod:`csv`.

Standard Markdown does not support tables, but Google Markdown as used in github does.
This layout lets you read and write that layout for text record processing.

.. py:class:: LineReader(iterable, **config)

    An :py:obj:`iterator` that returns strings parsed with :py:func:`split_escaped`.
    It skips rows which are header layoutting.

.. py:class:: DictReader(iterable[, fieldnames=None[, **config]])

    An :py:obj:`iterator` that returns strings parsed with :py:func:`split_escaped`.
    It is a subclass of :py:class:`DictReader` and reads the :py:attr:`fieldnames`
    from the header row if they have not been supplied.

.. py:class:: LineWriter(outfile, fieldnames, **config)

    An :py:class:`txf.layouts.LineWriter` that returns strings joined with :py:func:`join_escaped`.
    It skips rows which are header layoutting.

.. py:class:: DictWriter(outfile, fieldnames, **config)

    A :py:class:`txf.layouts.DictWriter` that

    .. py:method:: writeheader()

        Writes the Markdown header and underlines.

    .. py:method:: writerow(row)

        Writes the row in Markdown table layout.

    .. py:method:: writefooter()

        NOP
