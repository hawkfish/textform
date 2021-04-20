Limit: Filter rows using the row position
=========================================

.. py:currentmodule:: textform

.. py:class:: Limit(source=None[, limit=1[, offset=0]])

    The ``Limit`` transform filters out rows based on their position in the stream.

    .. py:attribute:: source
        :type: Transform or None

        The input pipeline.
        If one is not provided, ``Limit`` will generate *limit* empty rows.

    .. py:attribute:: limit
        :type: int

        The maximum number of input rows to pass through.

    .. py:attribute:: offset
        :type: int

        The number of input rows to skip before counting starts.

Usage:
^^^^^^

.. code-block:: python

   Limit(p, 10)
   Limit(p, 20, 10)

Example
^^^^^^^

.. csv-table::
   :file: limit_in_example.csv
   :header-rows: 1
   :quote: "
   :align: left

.. code-block:: python

   Limit(p, 10)

.. csv-table::
   :file: limit_example.csv
   :header-rows: 1
   :align: left
