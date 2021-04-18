Format
======

.. py:currentmodule:: textform

.. py:class:: Format(source, outputs, function)

    The ``Format`` transform reformats the values of a column using a user-supplied function.

    .. py:attribute:: source
        :type: Transform

        The input pipeline.

    .. py:attribute:: input
        :type: Transform

        The name of the string column to apply the *function* to.
        The contents will be replaced, so use :py:class:`Copy` to preserve the original.

    .. py:attribute:: function
        :type: callable

        A Python ``callable`` that receives the original value and returns the reformatted value.


Usage
^^^^^

.. code-block:: python

   Format(p, 'Year', lambda x: x+1)
