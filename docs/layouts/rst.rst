reStructured Text
=================

.. py:currentmodule:: txf.layouts.rst

The ``rst`` layout reads and writes records as *escaped* rst tables using an interface
that looks like :py:mod:`csv`.

reStructured Text has a facility for reading csv files as tables,
but the feature allows the embedding for layoutting inlayoution.
This makes it difficult to export literal tables for examples.
The :py:mod:`txf.layouts.rst` layoutter escapes layoutting inlayoution
before routing the result to the :py:mod:`txf.layouts.csv` module.

.. py:class:: LineReader(iterable, **config)

    An alias for :py:class:`csv.LineReader` .

.. py:class:: DictReader(iterable[, fieldnames=None[, **config]])

    An alias for :py:class:`csv.DictReader` .

.. py:class:: LineWriter(outfile, fieldnames, **config)

    A :py:class:`txf.layouts.LineWriter` that escapes ``rst`` layoutting directives.

   .. py:method:: writerow(values)

        Escapes the values before delegating them to a :py:class:`csv.LineWriter`.

.. py:class:: DictWriter(outfile, fieldnames, **config)

    A subclass of :py:class:`txf.layouts.csv.DictWriter` that escapes ``rst`` layoutting directives.

    .. py:method:: writerow(row)

        Escapes the values before passing them along to the base class.

    .. py:method:: writefooter()

        NOP
