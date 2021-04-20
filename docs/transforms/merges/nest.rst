Nest: Merge fields into a formatted string record
=================================================

.. py:currentmodule:: textform

.. py:class:: Nest(source, inputs, output[, format='csv'[, **config]])

    The ``Nest`` transform combines fields into a single string field using a particular format.
    ``Nest`` is the logical inverse of :py:class:`Unnest`.
    It is a subclass of :py:class:`Merge`.

    .. py:attribute:: source
        :type: Transform

        The input pipeline.

    .. py:attribute:: inputs
        :type: tuple(str) or str

        The fields to combine.
        They will be dropped from the output, so use :py:class:`Copy` to preserve them.

    .. py:attribute:: output
        :type: str

        The output field receiving the merged values.
        It cannot overwrite existing fields. Use :py:class:`Drop` to remove unwanted fields.

    .. py:attribute:: format
        :type: str

        The format to generate the output in.
        Supported nesting formats are:

        * ``csv`` Comma-separated string
        * ``json``, ``jsonl`` JavaScript Object Notation string
        * ``md`` GitHub Markdown row
        * ``text`` The Python string representation of the inputs as a list

    .. py:attribute:: config
        :type: kwargs

        Extra arguments to be passed to the formatting object.

Usage
^^^^^

.. code-block:: python

   Nest(p, ('F1', 'F2',) 'CSV', 'csv')
   Nest(p, ('Sales 1992', 'Sales 1993',) 'Dict', 'py')
