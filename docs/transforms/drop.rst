Drop
====

.. py:currentmodule:: textform

.. py:class:: Drop(source, inputs)

    The ``Drop`` transform removes columns from the records.

    .. py:attribute:: source
        :type: Transform

        The input pipeline (required).

    .. py:attribute:: inputs
        :type: tuple(str), str

        The name(s) of the columns to remove.

Usage
^^^^^

.. code-block:: python

   Drop(p, 'Invalid')
