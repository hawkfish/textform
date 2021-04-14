Limit
=====

The ``Limit`` transform filters out rows based on their position in the stream. Its arguments are

* *pipeline* The input pipeline. If one is not provided (``None``), ``Limit`` will generate *limit* empty rows.
* *limit* The maximum number of rows to pass. Defaults to ``1``.
* *offset* The number of rows to skip before counting.  Defaults to ``0``.

Examples:
^^^^^^^^^

.. code-block:: python
  
   Limit(p, 10)
   Limit(p, 20, 10)
