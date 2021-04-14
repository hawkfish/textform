Merge
=====

The ``Merge`` transform combines two or more columns into a single field. Its arguments are:

* *pipeline* The input pipeline (required).
* *inputs* The columns to combine. They will be dropped from the output, so use ``Copy`` to preserve them.
* *output* The output column receiving the merged values.
* *glue* Either a string used to join the input values, or a *callable*.
  If it is a *callable*, it will be given the values of *inputs* as positional arguments **in the given order**.

``Merge`` can be used with ``Divide`` to combine column variants that have been reformatted separately.

Examples:
^^^^^^^^^

.. code-block:: python
  
   Merge(p, ('US Date', 'UK Date',) 'Date', '')
   Merge(p, ('Sales 1992', 'Sales 1993',) 'Sales', operator.add)
