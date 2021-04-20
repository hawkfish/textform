Add: Insert constant fields
===========================

.. py:currentmodule:: textform

.. py:class:: Add(source, outputs, values)

    The ``Add`` transform adds one or more constant values to the record stream.

    .. py:attribute:: source
        :type: Transform

        If one is not provided (``None``), ``Add`` will generate identical rows indefinitely.

    .. py:attribute:: outputs
        :type: tuple(str), str

        The name(s) of the output fields.
        They cannot overwrite existing fields. Use :py:class:`Drop` to remove unwanted fields.

    .. py:attribute:: values
        :type: tuple

        The value(s) for the output fields. There must be the same number as *outputs*.

Usage
^^^^^

.. code-block:: python

    Add(p, 'InputFile', 'test.csv')
    Add(p, 'Timestamp', datetime.datetime.now()

Example
^^^^^^^

.. csv-table::
   :file: add_in_example.csv
   :header-rows: 1
   :quote: "
   :align: left

.. code-block:: python

   Add(p, 'Branch', 'master')

.. csv-table::
   :file: add_example.csv
   :header-rows: 1
   :align: left
