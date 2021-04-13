Cast
=======

The ``Cast`` transform casts the values in a column to a Python type. Its arguments are:

* *pipeline* The input pipeline (required).
* *input* The name of the string column to apply the *pattern* to. It will be replaced, so use ``Copy`` to preserve the original.
* *result_type* A Python type object (e.g., ``int``).
* *defaults* If the *pattern* does not match, the first output will contain the original string and the remaining outputs will be filled with the value(s) 
  in *defaults*. If *defaults* is not a single value, it must be the same size as the number of *outputs*.

Examples:
^^^^^^^^^

.. code-block:: python

   Cast(p, 'Year', int)
   Cast(p, 'Timestamp', datetime.datetime)
