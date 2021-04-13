Lag
===

The ``Lag`` transform shifts the values of a column up or down. Negative lags are sometimes called "leads", but ``Lag`` handles both cases.
Its arguments are:

* *pipeline* The input pipeline (required).
* *input* The name of the string column to apply the *pattern* to. It will be replaced, so use ``Copy`` to preserve the original.
* *lag* An integer specifying how many rows to lag (delay) the column by. A negative lag will cause later values to be pulled forward.
  Zero is legal, but a NOP.

Examples:
^^^^^^^^^

.. code-block:: python

   Lag(p, 'Previous', 1)
   Lag(p, 'Next', -1
