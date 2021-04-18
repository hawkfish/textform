Fill
====

.. py:currentmodule:: textform

.. py:class:: Fill(source, input[, default=''[, blank='']])

    The ``Fill`` (or ``FillDown``) transform fills in blank values by using the most recent value for the column.
    ``Fill`` is a subclass of :py:class:`Format` because it effectively reformats a column.

    .. py:attribute:: source
        :type: Transform

        The input pipeline.

    .. py:attribute:: input
        :type: str

        The name of the column to fill in.
        The contents will be replaced, so use :py:class:`Copy` to preserve the original.

    .. py:attribute:: default
        :type: any

        The value to use when there is no most recent value (e.g, at the top of the file).
        It needs to match the type of the column.

    .. py:attribute:: blank
        :type: any

        The value to use to determine "blankness" (e.g., for non-string columns it might be ``0`` or ``None``).

Usage
^^^^^

.. code-block:: python

   Fill(p, 'State')
   Fill(p, 'Amount', 0.0, 0.0)

Example
^^^^^^^

.. csv-table::
   :file: divide_example.csv
   :header-rows: 1
   :quote: "
   :align: left

.. code-block:: python

   Fill(p, 'Query', 'Q00')

.. csv-table::
   :file: fill_example.csv
   :header-rows: 1
   :align: left
