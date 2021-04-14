Cast
====

The ``Cast`` transform casts the values in a column to a Python type. Its arguments are:

* *pipeline* The input pipeline (required).
* *input* The name of the string column to apply the *pattern* to. It will be replaced, so use ``Copy`` to preserve the original.
* *result_type* A Python type object (e.g., ``int``).

``Cast`` is a special case of ``Format``.

Examples:
^^^^^^^^^

.. code-block:: python

   Cast(p, 'Year', int)
   Cast(p, 'Timestamp', datetime.datetime)
