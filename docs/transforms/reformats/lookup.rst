Lookup: Replace a value with one from a lookup table
====================================================

.. py:currentmodule:: txf

.. py:class:: Lookup(source, outputs, table[, missing=None])

    The ``Lookup`` transform replaces field values with the corresponding values in a table.
    The mapped values do not have to be the same type.
    ``Lookup`` is a subclass of :py:class:`Format`.

    .. py:attribute:: source
        :type: Transform

        The input pipeline.

    .. py:attribute:: input
        :type: str

        The name of the field to use to search the table.
        The contents will be replaced, so use :py:class:`Copy` to preserve the original.

    .. py:attribute:: table
        :type: dict

        A Python dictionary whose keys are the values of *input*.

    .. py:attribute:: missing
        :type: any

        The value to use if the *input* value is not found in the *table*.
        It must have the same type as the table values.

Usage
^^^^^

.. code-block:: python

   Lookup(p, 'State', {'CA': 'California'}, 'Unknown')
   Lookup(p, 'Month', {'Jan': 1}, 0)
