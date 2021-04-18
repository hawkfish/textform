Lookup
======

.. py:currentmodule:: textform

.. py:class:: Lookup(source, outputs, values)

    The ``Lookup`` transform replaces column values with the corresponding values in a table.
    The mapped values do not have to be the same type.
    ``Lookup`` is a subclass of :py:class:`Format`.

    .. py:attribute:: source
        :type: Transform

        The input pipeline.

    .. py:attribute:: input
        :type: str

        The name of the column to use to search the table.
        The contents will be replaced, so use :py:class:`Copy` to preserve the original.

    .. py:attribute:: table
        :type: dict

        A Python dictionary whose keys are the values of *input*.

    .. py:attribute:: default
        :type: any

        The value to use if the *input* value is not found in the *table*.
        It must have the same type as the table values.


Usage
^^^^^

.. code-block:: python

   Lookup(p, 'State', {'CA': 'California'}, 'Unknown')
   Lookup(p, 'Month', {'Jan': 1}, 0)
