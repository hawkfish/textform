Fill
====

The ``Fill`` (or ``FillDown``) transform fills in missing values by using the most recent value for the column. Its arguments are:

* *pipeline* The input pipeline (required).
* *input* The name of the column to apply the *predicate* to. It will be dropped from the output, so use ``Copy`` to preserve it.
* *default* The value to use when there is no most recent value (e.g, at the top of the file). Defaults to the empty string.
* *blank* The value to use to determine "blankness" (e.g., for non-string columns it might be ``0`` or ``None``). Defaults to the empty string.

``Fill`` is a subclass of ``Format`` because it reformats a column.

Examples:
^^^^^^^^^

.. code-block:: python
  
   Fill(p, 'State')
   Fill(p, 'Amount', 0.0, 0.0)
