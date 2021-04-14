Text
=====

The ``Text`` transform pulls lines from an ``iterable`` in ``text`` format. Its arguments are:

* *iterable* The input. Each row will be generated from the result ``next(iterable)``.
* *output* The name of the output column containing the lines. It cannot overwrite existing columns. Use ``Drop`` to remove unwanted columns.
* *pipeline* An optional input pipeline. New rows will be merged with the output of this pipeline.

``Text`` is a subclass of ``Read``.

Examples:
^^^^^^^^^

.. code-block:: python

   Text(sys.stdin)
   Text(['Line 1', 'Line 2',], Sequence(None, 'Row #', 1))
