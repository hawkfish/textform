Lift
====

The ``Lift`` (or ``FillUp``) transform fills in missing values by using the next non-blank value for the column. Its arguments are:

* *pipeline* The input pipeline (required).
* *input* The name of the column to apply the *predicate* to. It will be dropped from the output, so use ``Copy`` to preserve it.
* *default* The value to use when there is no most recent value (e.g, at the top of the file). Defaults to the empty string.
* *blank* The value to use to determine "blankness" (e.g., for non-string columns it might be ``0`` or ``None``). Defaults to the empty string.

``Lift`` is a logical form of ``Format`` because it reformats a column, but it is not a subclass. 
It is so named because "lift" is roughly "fill" spelled backwards, and it suggests the operation.

Examples:
^^^^^^^^^

.. code-block:: python
  
   Lift(p, 'State')
   Lift(p, 'Total', 0.0, 0.0)
