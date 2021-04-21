Match: Filter rows using a regular expression
=============================================

.. py:currentmodule:: txf

.. py:class:: Match(source, input, pattern[, invert=False])

    The ``Match`` transform filters rows based on a regular expression.
    ``Match`` is a subclass of :py:class:`Select`.

    .. py:attribute:: source
        :type: Transform

        The input pipeline.

    .. py:attribute:: input
        :type: str

        The name of the column to apply the *pattern* to.

    .. py:attribute:: pattern
        :type: str

        A regular expression to match against the *input*.

    .. py:attribute:: invert
        :type: Boolean

        Negative matching is difficult to specify with regular expressions,
        so this lets the caller reject rows that match a pattern.


Usage
^^^^^

.. code-block:: python

   Match(p, 'Date', r'(\d+)/(\d+)/(\d+)') # Filter to valid dates
   Match(p, 'Line', '-----', True)        # Exclude formatting lines

Example
^^^^^^^

.. csv-table::
   :file: match_in_example.csv
   :header-rows: 1
   :quote: "
   :align: left

.. code-block:: python

   Match(p, 'Line', '-----', True)

.. csv-table::
   :file: match_example.csv
   :header-rows: 1
   :align: left

