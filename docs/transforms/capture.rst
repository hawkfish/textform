Capture
=======

The ``Capture`` transform replaces a string column with the capture groups from a regular expression. Its arguments are:

* *pipleline* The input pipeline (required).
* *input* The name of the string column to apply the *pattern* to. It will be dropped from the output, so use ``Copy`` to preserve it.
* *outputs* The the output columns receiving the capture groups. There must be the same number as the number of capture groups in the *pattern*.
  *input* is a valid name for an output.
* *pattern* A regular expression with capture groups.
* *defaults* If the *pattern* does not match, the first output will contain the original string and the remaining outputs will be filled with the value(s) 
  in *defaults*. If *defaults* is not a single value, it must be the same size as the number of *outputs*.

Examples:
^^^^^^^^^

.. code-block:: python
  Capture(p, 'Date', ('Month', 'Day', 'Year',), r'(\d+)/(\d+)/(\d+)')
  Capture(p, 'Query', 'Query', r'Q(\d+)')
