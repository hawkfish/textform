Read: Import record data from an iterable using a layout
========================================================

.. py:currentmodule:: txf

.. py:class:: Read(iterable, [source=None[, layout='csv'[, **config]]])

    The ``Read`` transform pulls records from an ``iterable`` using a particular layout.
    The output field names will be determined from the input or the *config* parameters.
    ``Read`` is the logical inverse of :py:class:`Write`.

    .. py:attribute:: iterable
        :type: iterable

        The input. Each row will be generated from the result of ``next(iterable)``.

    .. py:attribute:: source
        :type: Transform or None

        An optional input pipeline.
        New rows will be merged with the output of this pipeline.

    .. py:attribute:: layout
        :type: str

        The layout to generate the output in. Supported read layouts are:

        * ``csv`` Comma-separated values. The header will be read to provide the field names.
        * ``json`` JavaScript Object Notation records in array layout (``[{..},...]``)
        * ``jsonl`` JavaScript Object Notation Line layout (``{...}\n{...}\n...``)
        * ``md`` GitHub Markdown tables with headers
        * ``text`` Treats the file as a single field with a name taken from ``config['default_fieldnames']``.

    .. py:attribute:: config
        :type: kwargs

        Extra arguments to be passed to the layout object.

Usage
^^^^^

.. code-block:: python

   Read(p, sys.stdin 'csv')
   Read(p, records, 'jsonl')
