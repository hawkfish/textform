Split
=====

The ``Split`` transform replaces a column with a set of values generated from the inputs. Its arguments are:

* *pipeline* The input pipeline (required).
* *input* The name of the string column to apply the *pattern* to. It will be dropped from the output, so use ``Copy`` to preserve it.
* *outputs* The the output columns receiving the split values.
* *separator* Either a string or a *callable* used to split up the column. 
  If it is a *callable*, it will be passed the value as a single argument and should return an array of values.
* *defaults* The value(s) to be used for missing strings when *separator* is a string.

Examples:
^^^^^^^^^

.. code-block:: python
  
   Split(p, 'Date', ('Month', 'Day', 'Year',), r'/')
   Split(p, 'Year', ('Century' 'Decade', 'Year',), lambda y: [y // 100, (y % 100) // 10, y % 10])
