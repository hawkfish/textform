Split
=====

.. py:currentmodule:: textform

.. py:class:: Split(source, input, outputs, separator, defaults)

    The ``Split`` transform replaces a column with a set of values generated from the inputs.

    .. py:attribute:: source
        :type: Transform

        The input pipeline.

    .. py:attribute:: input
        :type: str

        The name of the column to split.
        It will be dropped from the output, so use :py:class:`Copy` if you need to preserve it.


    .. py:attribute:: outputs
        :type: tuple(str), str

        The output column(s) receiving the split values.
        They cannot overwrite existing columns. Use :py:class:`Drop` to remove unwanted columns.

    .. py:attribute:: separator
        :type: str or callable

        Either a string or a ``callable`` used to split up the column.
        If it is a string, the value will be split using ``str.split``.
        If it is a ``callable``, it will be passed the value as a single argument
        and should return a ``list`` of values in the order of the outputs.

    .. py:attribute:: defaults
        :type: tuple

        The value(s) to be used for missing elements of the *separator* result.

Usage
^^^^^

.. code-block:: python

   Split(p, 'Date', ('Month', 'Day', 'Year',), r'/')
   Split(p, 'Year', ('Century' 'Decade', 'Year',), lambda y: [y // 100, (y % 100) // 10, y % 10])

Example
^^^^^^^

.. csv-table::
   :file: split_in_example.csv
   :header-rows: 1
   :quote: "
   :align: left

.. code-block:: python

   Split(p, 'Query', ('Query', 'Mode',), '_', ('00', 'SERIAL',))

.. csv-table::
   :file: split_example.csv
   :header-rows: 1
   :align: left
