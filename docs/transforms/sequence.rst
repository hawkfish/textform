Sequence
========

The ``Sequence`` transform generate a sequence of integers. Its arguments are:

* *pipeline* The input pipeline. If one is not provided (``None``), ``Add`` will generate rows indefinitely.
* *output* The name of the output column. It cannot overwrite existing columns. Use ``Drop`` to remove unwanted columns.
* *start* The start value for the sequence. Default: ``0``.
* *step* The increment amount for each record. Default: ``1``.

Examples:
^^^^^^^^^

.. code-block:: python

   Sequence(p, 'Row #', 1)
   Sequence(p, 'Even', 0, 2)
