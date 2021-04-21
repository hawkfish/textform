Merge: Combine multiple fields into one
=======================================

.. py:currentmodule:: txf

.. py:class:: Merge(source, inputs, output[, glue=''])

    The ``Merge`` transform combines two or more fields into a single field.
    ``Merge`` can be used with :py:class:`Divide` to combine field variants that have been
    reformatted separately into a single representation

    .. py:attribute:: source
        :type: Transform

        The input pipeline.

    .. py:attribute:: inputs
        :type: tuple(str), str

        The fields to combine.
        They will be dropped from the output, so use :py:class:`Copy` to preserve them.

    .. py:attribute:: output
        :type: str

        The output field receiving the merged values.
        It cannot overwrite existing fields, so use :py:class:`Drop` to remove unwanted fields.

    .. py:attribute:: glue
        :type: str or callable

        Either a string used to join the input values, or a *callable*.
        If the glue is a *callable*, it will be given the values of *inputs* as positional arguments
        **in the given order**.
        It should return the merged value.


Usage
^^^^^

.. code-block:: python

   Merge(p, ('US Date', 'UK Date',) 'Date', '')
   Merge(p, ('Sales 1992', 'Sales 1993',) 'Sales', operator.add)
