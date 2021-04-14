Lookup
======

The ``Lookup`` transform replaces column values with the corresponding values in a table. The mapped values do not have to be the same type.
Its arguments are:

* *pipeline* The input pipeline (required).
* *input* The name of the string column to apply the *pattern* to. It will be replaced, so use ``Copy`` to preserve the original.
* *table* A Python *dict* whose keys are the values of *input*.
* *default* The value to use if the *input* value is not found in the *table*.

``Lookup`` is a subclass of ``Format``.

Examples:
^^^^^^^^^

.. code-block:: python

   Lookup(p, 'State', {'CA': 'California'}, 'Unknown')
   Lookup(p, 'Month', {'Jan': 1}, 0)
