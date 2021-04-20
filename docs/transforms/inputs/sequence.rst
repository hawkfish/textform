Sequence: generate an integer sequence column
=============================================

.. py:currentmodule:: textform

.. py:class:: Sequence(source, output[, [start=0, step=1]])

    The ``Sequence`` transform generate a sequence of integers. Its arguments are:

    .. py:attribute:: source
        :type: Transform or None

        The input pipeline.
        If one is not provided, ``Sequence`` will generate rows indefinitely.

    .. py:attribute:: output
        :type: str

        The name of the output column.
        It cannot overwrite existing columns.
        Use :py:class:`Drop` to remove unwanted columns.

    .. py:attribute:: start
        :type: int

        The start value for the sequence.
        Note that it defaults to zero, not one.

    .. py:attribute:: step
        :type: int

        The increment amount for each record.

Usage
^^^^^

.. code-block:: python

   Sequence(p, 'Row #', 1)
   Sequence(p, 'Even', 0, 2)
