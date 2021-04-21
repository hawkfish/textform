Drop: Remove unneeded fields
============================

.. py:currentmodule:: txf

.. py:class:: Drop(source, inputs)

    The ``Drop`` transform removes fields from the records.

    .. py:attribute:: source
        :type: Transform

        The input pipeline (required).

    .. py:attribute:: inputs
        :type: tuple(str), str

        The name(s) of the fields to remove.

Usage
^^^^^

.. code-block:: python

   Drop(p, 'Invalid')
