Format
======

The ``Format`` transform reformats the values of a column. Its arguments are:

* *pipeline* The input pipeline (required).
* *input* The name of the string column to apply the *function* to. It will be replaced, so use ``Copy`` to preserve the original.
* *function* A Python ``callable`` that returns the reformatted value.

``Format`` differs from ``Cast`` because the result type has to be inferred at runtime.

Examples:
^^^^^^^^^

.. code-block:: python

   Format(p, 'Year', addone)
