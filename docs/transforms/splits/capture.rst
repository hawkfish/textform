Capture: Split a string into capture groups
===========================================

.. py:currentmodule:: textform

.. py:class:: Capture(source, input, outputs, pattern[, defaults = ''])

    The ``Capture`` transform replaces a string column with the capture groups from a regular expression.
    ``Capture`` is a subclass of :py:class:`Split`.

    .. py:attribute:: source
        :type: Transform

        The input pipeline.

    .. py:attribute:: input
        :type: str

        The name of the string column to apply the *pattern* to.
        It will be dropped from the output, so use :py:class:`Copy` to preserve it.

    .. py:attribute:: outputs
        :type: tuple(str), str

        The the output column(s)s receiving the capture groups.
        There must be the same number as the number of capture groups in the *pattern*.

    .. py:attribute:: pattern
        :type: str

        A regular expression with one or more capture groups.

    .. py:attribute:: defaults
        :type: tuple(str), str

        If the pattern does not match, the first output will contain the original string
        and the remaining *outputs* will be filled with the value(s) in *defaults*.
        If *defaults* is not a single value, it must be the same size as the number of *outputs*.


Usage
^^^^^

.. code-block:: python

   Capture(p, 'Date', ('Month', 'Day', 'Year',), r'(\d+)/(\d+)/(\d+)')
   Capture(p, 'Query', 'Query', r'Q(\d+)')

Example
^^^^^^^

.. csv-table::
   :file: capture_in_example.csv
   :header-rows: 1
   :align: left

.. code-block:: python

   Capture(p, 'Run', ('Run #', 'Run Count', 'Time',), r'(\d+)/(\d+)...(\d+\.\d+)')

.. csv-table::
   :file: capture_example.csv
   :header-rows: 1
   :align: left
