Divide
======

The ``Divide`` transform separates a column into two fields, one containing the values that pass a predicate and the other containing the ones that fail. 
If the predicates is a regular expression, it will be used as the predicate. Its arguments are:

* *pipeline* The input pipeline (required).
* *input* The name of the column to apply the *predicate* to. It will be dropped from the output, so use ``Copy`` to preserve it.
* *passed* The output column receiving the values that pass the predicate.
* *failed* The output column receiving the values that fail the predicate.
* *predicate* A *callable* predicate or a regular expression.
* *fills* The value(s) to be used for the column that does not recieve the *input* value.

``Divide`` can be used to separate a column with multiple formats, find erroneous values or pull sections names out from the main data.

Examples:
^^^^^^^^^

.. code-block:: python
  
   Divide(p, 'Date', ('Date', 'Invalid',), r'(\d+)/(\d+)/(\d+)')
   Divide(p, 'Line', ('Query', 'Run',), r'Q(\d+)')
