Project: Compute a function value as a new field
================================================

.. py:currentmodule:: txf

.. py:class:: Project(source, inputs, output, function)

    The ``Project`` transform computes (projects) a new field
    using an arbitrary function of zero or more input fields.

    .. py:attribute:: source
        :type: Transform

        The input pipeline (required).

    .. py:attribute:: inputs
        :type: tuple(str) or str

        The fields to combine.
        They will *not* be dropped from the output.
        Note that nullary functions are supported.

    .. py:attribute:: output
        :type: str

        The field containing the computed result.

    .. py:attribute:: function
        :type: callable

        A *callable* implementing the function.
        It will be given the values of *inputs* as positional arguments **in the given order**.

Usage
^^^^^

.. code-block:: python

   Project(p, 'Number', 'Square', lambda x: x*x)
   Project(p, () 'Roll', rand.randint(1,6))
