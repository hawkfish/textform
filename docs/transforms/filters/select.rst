Select: Filter rows using a callable predicate
==============================================

.. py:currentmodule:: txf

.. py:class:: Select(source, inputs, predicate)

    The ``Select`` transform filters rows based on a predicate.

    .. py:attribute:: source
        :type: Transform

        The input pipeline.

    .. py:attribute:: inputs
        :type: tuple(str) or str

        The columns to use in the predicate.
        They will *not* be dropped from the output.

    .. py:attribute:: predicate
        :type: callable

        A ``callable`` implementing the predicate.
        It will be given the values of *inputs* as positional arguments **in the given order**.
        the result will be treated as a Boolean.

Usage
^^^^^

.. code-block:: python

   Select(p, 'Sales', lambda sales: sales > 0)
