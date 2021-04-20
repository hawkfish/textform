Divide
======

.. py:currentmodule:: textform

.. py:class:: Divide(source, outputs, values)

    The ``Divide`` transform separates a column into two fields,
    one containing the values that pass a predicate
    and the other containing the ones that fail.
    If the predicate is a regular expression, matching it will be used as the predicate.

    ``Divide`` can be used to separate a column with multiple formats,
    find erroneous values or
    pull sections names out from the main data.

    .. py:attribute:: source
        :type: Transform

        The input pipeline (required).

    .. py:attribute:: input
        :type: str

        The name of the column to apply the *predicate* to.
        It will be dropped from the output, so use :py:class:`Copy` to preserve it.

    .. py:attribute:: passed
        :type: str

        The output column receiving the values that pass the predicate.
        It cannot overwrite existing columns, so use :py:class:`Drop` to remove unwanted columns.

    .. py:attribute:: failed
        :type: str

        The output column receiving the values that fail the predicate.
        It cannot overwrite existing columns, so use :py:class:`Drop` to remove unwanted columns.

    .. py:attribute:: predicate
        :type: str or callable

        A callable predicate or a regular expression.

    .. py:attribute:: fills
        :type: str or tuple(str)

        The value(s) to be used for the column that does not recieve the *input* value.


Usage
^^^^^

.. code-block:: python

   Divide(p, 'Date', ('Date', 'Invalid',), r'(\d+)/(\d+)/(\d+)')
   Divide(p, 'Line', ('Query', 'Run',), r'Q(\d+)')

Example
^^^^^^^

.. csv-table::
   :file: divide_in_example.csv
   :header-rows: 1
   :quote: "
   :align: left

.. code-block:: python

   Divide(p, 'Line', 'Query', 'Run', 'Q')

.. csv-table::
   :file: divide_example.csv
   :header-rows: 1
   :align: left

