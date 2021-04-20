Google Markdown
===============

.. py:currentmodule:: textform.formats.md

The ``md`` format reads and writes records  as Markdown tables using an interface
that looks like :py:mod:`csv`.

Standard Markdown does not support tables, but Google Markdown as used in github does.
This format lets you read and write that format for text record processing.

.. py:class:: LineReader(iterable, **config)

    An :py:obj:`iterator` that returns strings parsed with :py:func:`split_escaped`.
    It skips rows which are header formatting.

.. py:class:: DictReader(iterable[, fieldnames=None[, **config]])

    An :py:obj:`iterator` that returns strings parsed with :py:func:`split_escaped`.
    It is a subclass of :py:class:`DictInput` and reads the :py:attr:`fieldnames`
    from the header row if they have not been supplied.

.. py:class:: LineWriter(outfile, fieldnames, **config)

    An :py:class:`textform.formats.LineWriter` that returns strings joined with :py:func:`join_escaped`.
    It skips rows which are header formatting.

.. py:class:: DictWriter(outfile, fieldnames, **config)

    A :py:class:`textform.formats.DictWriter` that

    .. py:method:: writeheader()

        Writes the Markdown header and underlines.

    .. py:method:: writerow(row)

        Writes the row in Markdown table format.

    .. py:method:: writefooter()

        NOP

.. py:function:: split_escaped(field[, sep='|'[, esc='\\']])

    Implements a state machine to split escaped strings using a separator and an escape character.

    :returns: A :py:obj:`tuple` of split strings.

.. py:function:: join_escaped(values[, sep='|'[, esc='\\']])

    Escapes the strings and joins them.

    :returns: A :py:obj:`str` containing the escaped line.
