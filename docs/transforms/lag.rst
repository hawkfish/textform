Lag
===

.. py:currentmodule:: textform

.. py:class:: Lag(self, source, input[, lag=1[, default='']])

    The ``Lag`` transform shifts the values of a column up or down.
    Negative lags are sometimes called "leads", but ``Lag`` handles both cases.
    ``Lag`` is a logical version of :py:class:`Format` because it recomputes the values
    of a column, but it is not a subclass.

    .. py:attribute:: source
        :type: Transform

        The input pipeline.

    .. py:attribute:: input
        :type: str

        The name of the string column to lag or lead.
        The contents will be replaced, so use :py:class:`Copy` to preserve the original.

    .. py:attribute:: lag
        :type: int

        An integer specifying how many rows to lag (delay) the column by.
        A negative lag will cause later values to be pulled forward.
        Zero is legal, but a NOP.

    .. py:attribute:: default
        :type: any

        The value to use when there is no most recent value (e.g, at the top of the file).
        It needs to match the type of the column.

Usage
^^^^^

.. code-block:: python

   Lag(p, 'Previous', 1)
   Lag(p, 'Next', -1
