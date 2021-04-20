Text Lines
==========

.. py:currentmodule:: textform.formats.text

The ``text`` format reads and writes records as single lines of text using an interface
that looks like :py:mod:`csv`.

.. py:class:: LineReader(iterable, **config)

    An :py:obj:`iterator` that returns strings with the line separator removed.

.. py:class:: DictReader(iterable[, fieldnames=None[, **config]])

    An :py:obj:`iterator` that returns single lines.
    ``fieldnames`` will be truncated to a single value.
    if it is not provided, the ``default_fieldnames`` entry from ``config`` will be used.

.. py:class:: LineWriter(outfile, fieldnames, **config)

    An :py:class:`textform.formats.LineWriter` that returns strings joined with :py:func:`join_escaped`.
    It skips rows which are header formatting.

    .. py:method:: writerow(row)

        Writes the row by casting it to a string.

.. py:class:: DictWriter(outfile, fieldnames, **config)

    A :py:class:`textform.formats.DictWriter` that

    .. py:method:: writeheader()

        NOP

    .. py:method:: writerow(row)

        Writes the row as a single string value.

    .. py:method:: writefooter()

        NOP
