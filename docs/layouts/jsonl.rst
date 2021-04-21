JavaScript Object Notation Lines
================================

.. py:currentmodule:: txf.layouts.jsonl

The ``jsonl`` layout uses the :py:mod:`json` module to read and write records using an interface
that looks like :py:mod:`csv`.

The difference between strict JSON and line-oriented JSON (:py:mod:`jsonl`)
is that line-oriented JSON writes out each records on a separate line.

.. py:class:: LineReader(iterable, **config)

    An :py:obj:`iterator` that returns strings parsed with :py:meth:`json.loads`.

.. py:class:: DictReader(iterable, fieldnames=None, **config)

    An :py:obj:`iterator` that returns strings parsed with :py:meth:`json.loads`.
    It is a subclass of :py:class:`DictInput` and reads the :py:attr:`fieldnames`
    from the first record if they have not been supplied.

.. py:class:: LineWriter(outfile, fieldnames, **config)

    This is simply an alias for :py:class:`txf.layouts.jsonl.LineWriter`.

    .. py:method:: writerow(values)

        Writes the the ``values`` as a JSON record using the :py:attr:`fieldnames` as keys.

.. py:class:: DictWriter(outfile, fieldnames, **config)

    A :py:class:`txf.layouts.DictWriter` that writes JSON records, one per line.

    .. py:method:: writeheader()

        NOP.

    .. py:method:: writerow(row)

        Writes the row in JSON layout with a newline.

    .. py:method:: writefooter()

        NOP

