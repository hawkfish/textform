Add
===

The ``Add`` transform adds one or more constant values to the record stream. Its arguments are

* *pipeline* The input pipeline. If one is not provided (``None`), ``Add`` will generate rows indefinitely.
* *outputs* The name(s) of the output columns. They cannot overwrite input columns. Use ``Drop`` to remove unwanted columns.
* *values* The value(s) for the output columns. There must be the same number as *outputs*.

Examples:
^^^^^^^^^

.. code-block:: python
  
   Add(p, 'InputFile', 'test.csv')
   Add(p, 'Timestamp', datetime.datetime.now()
