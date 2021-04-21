Copy: Duplicate fields
======================

.. py:currentmodule:: txf

.. py:class:: Copy(pipeline, input, outputs)

    The ``Copy`` transform makes one or more duplicates of a field.

    .. py:attribute:: pipeline
        :type: Transform

        The input pipeline (required).

    .. py:attribute:: input
        :type: str

        The name of the field to duplicate. It will be *not* be removed.

    .. py:attribute:: outputs
        :type: tuple(str)

        One or more fields to receive the copies.
        They cannot overwrite existing fields, so use :py:class:`Drop` to remove unwanted fields.

Usage
^^^^^

.. code-block:: python

   Copy(p, 'Year', 'Last Year')
   Copy(p, 'Original', ('Dupe 1', 'Dupe 2',))
