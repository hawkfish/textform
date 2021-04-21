Lift: Fill in missing values by copying up
==========================================

.. py:currentmodule:: txf

.. py:class:: Lift(source, input[, default=''[, blank='']])

    The ``Lift`` (or ``FillUp``) transform fills in missing values by using the *next* non-blank value for the field.
    ``Lift`` is a logical form of :py:class:`Format` because it reformats a field, but it is not a subclass.
    It is so named because "lift" is roughly "fill" spelled backwards, which suggests the operation.

    .. py:attribute:: source
        :type: Transform

        The input pipeline.

    .. py:attribute:: input
        :type: str

        The name of the field to fill in.
        The contents will be replaced, so use :py:class:`Copy` to preserve the original.

    .. py:attribute:: default
        :type: any

        The value to use when there is no most recent value (e.g, at the top of the file).
        It needs to match the type of the field.

    .. py:attribute:: blank
        :type: any

        The value to use to determine "blankness" (e.g., for non-string fields it might be ``0`` or ``None``).

Usage
^^^^^

.. code-block:: python

   Lift(p, 'State')
   Lift(p, 'Total', 0.0, 0.0)
