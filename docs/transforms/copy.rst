Copy
====

.. py:class:: Copy(pipeline, input, outputs)

    The ``Copy`` transform makes one or more duplicates of a field.

.. py:attribute:: pipeline
    :type: Transform
    :noindex:

    The input pipeline (required).

.. py:attribute:: input
    :type: str
    :noindex:

    The name of the field to duplicate. It will be *not* be removed.

.. py:attribute:: outputs
    :type: tuple(str)
    :noindex:

    One or more fields to receive the copies.

Examples:
^^^^^^^^^

.. code-block:: python

   Copy(p, 'Year', 'Last Year')
   Copy(p, 'Original', ('Dupe 1', 'Dupe 2',))
