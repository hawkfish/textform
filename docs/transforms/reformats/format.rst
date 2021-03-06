Format: Replace a value with a computed value
=============================================

.. py:currentmodule:: txf

.. py:class:: Format(source, outputs, function)

    The ``Format`` transform reformats the values of a field using a user-supplied function.

    .. py:attribute:: source
        :type: Transform

        The input pipeline.

    .. py:attribute:: input
        :type: Transform

        The name of the string field to apply the *function* to.
        The contents will be replaced, so use :py:class:`Copy` to preserve the original.

    .. py:attribute:: function
        :type: callable

        A Python ``callable`` that receives the original value and returns the reformatted value.


Usage
^^^^^

.. code-block:: python

   Format(p, 'Year', lambda x: x+1)
