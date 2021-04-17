Cast
====

.. py:currentmodule:: textform

.. py:class:: Cast(source, input, result_type)

    The ``Cast`` transform casts the values in a column to a Python type.
    ``Cast`` is a special case of ``Format``.

    .. py:attribute:: source
        :type: Transform

        The input pipeline.

    .. py:attribute:: input
        :type: str

        The name of the column to cast.
        It will be replaced, so use :py:class:`Copy` to preserve the original.

    .. py:attribute:: result_type
        :type: type

        A Python type object to perform the cast.

Examples:
^^^^^^^^^

.. code-block:: python

   Cast(p, 'Year', int)
   Cast(p, 'Timestamp', datetime.datetime)


Example
^^^^^^^

.. csv-table::
   :file: split_example.csv
   :header-rows: 1
   :quote: "
   :align: left

.. code-block:: python

   Cast(p, 'Query', int)

.. csv-table::
   :file: cast_example.csv
   :header-rows: 1
   :align: left
