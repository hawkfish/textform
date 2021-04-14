Select
======

The ``Select`` transform filters rows based on a predicate. Its arguments are:

* *pipeline* The input pipeline (required).
* *inputs* The columns to use in the predicate. They will *not* be dropped from the output.
* *predicate* A ``callable`` implementing the predicate.
  It will be given the values of *inputs* as positional arguments **in the given order**.

Examples:
^^^^^^^^^

.. code-block:: python

   Select(p, 'Sales', lambda sales: sales > 0)
