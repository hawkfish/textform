Cast: Change the data type of a field
=====================================

.. py:currentmodule:: textform

.. py:class:: Cast(source, input, result_type)

    The ``Cast`` transform casts the values in a field to a Python type.
    ``Cast`` is a special case of :py:class:`Format`.

    .. py:attribute:: source
        :type: Transform

        The input pipeline.

    .. py:attribute:: input
        :type: str

        The name of the field to cast.
        The contents will be replaced, so use :py:class:`Copy` to preserve the original.

    .. py:attribute:: result_type
        :type: type

        A Python type object to perform the cast.

Usage
^^^^^

.. code-block:: python

   Cast(p, 'Year', int)
   Cast(p, 'Timestamp', datetime.datetime)


Example
^^^^^^^

.. csv-table::
   :file: cast_in_example.csv
   :header-rows: 1
   :quote: "
   :align: left

.. code-block:: python

   Cast(p, 'Query', int)

.. csv-table::
   :file: cast_example.csv
   :header-rows: 1
   :align: left
