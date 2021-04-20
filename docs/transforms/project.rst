Project: Compute a function value as a new column
=================================================

.. py:currentmodule:: textform

.. py:class:: Project(source, inputs, output, function)

    The ``Project`` transform computes (projects) a new column
    using an arbitrary function of zero or more input columns.

    .. py:attribute:: source
        :type: Transform

        The input pipeline (required).

    .. py:attribute:: inputs
        :type: tuple(str) or str

        The columns to combine.
        They will *not* be dropped from the output.
        Note that nullary functions are supported.

    .. py:attribute:: output
        :type: str

        The column containing the computed result.

    .. py:attribute:: function
        :type: callable

        A *callable* implementing the function.
        It will be given the values of *inputs* as positional arguments **in the given order**.

Usage
^^^^^

.. code-block:: python

   Project(p, 'Number', 'Square', lambda x: x*x)
   Project(p, () 'Roll', rand.randint(1,6))
