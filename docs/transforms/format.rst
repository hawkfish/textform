Format
======

The ``Format`` transform reformats the values of a column. Its arguments are:

* *pipeline* The input pipeline (required).
* *input* The name of the string column to apply the *pattern* to. It will be replaced, so use ``Copy`` to preserve the original.
* *function* A Python *callable* that formats the column.

``Format`` differs from ``Cast`` because the resulttype has to be inferred at runtime.

Examples:
^^^^^^^^^

.. code-block:: python

   Format(p, 'Year', addone)
