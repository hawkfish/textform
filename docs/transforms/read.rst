Read
=====

.. py:currentmodule:: textform

.. py:class:: Read(iterable, [source=None, [, format='csv', **config]]])

    The ``Read`` transform pulls records from an ``iterable`` using a particular format.
    ``Read`` is the logical inverse of :py:class:`Write`.

    .. py:attribute:: iterable
        :type: iterable

        The input. Each row will be generated from the result of ``next(iterable)``.

    .. py:attribute:: source
        :type: Transform or None

        An optional input pipeline.
        New rows will be merged with the output of this pipeline.

    .. py:attribute:: format
        :type: str

        The format to generate the output in. Supported read formats are:

        * ``csv`` Comma-separated values. The header will be read to provide the column names.
        * ``json`` JavaScript Object Notation records in array format (``[{..},...]``)
        * ``jsonl`` JavaScript Object Notation Line format (``{...}\n{...}\n...``)
        * ``md`` GitHub Markdown tables with headers
        * ``text`` Treats the file as a single column with a name taken from ``config['default_fieldnames']``.

    .. py:attribute:: config
        :type: kwargs

        Extra arguments to be passed to the formatting object.

Usage
^^^^^

.. code-block:: python

   Read(p, sys.stdin 'csv')
   Read(p, records, 'jsonl')
