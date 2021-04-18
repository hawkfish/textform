Iterate
=======

.. py:currentmodule:: textform

.. py:class:: Iterate(pipeline, input, tags, values[, format='csv'[, **config]])

    The ``Iterate`` transform is a cross between :py:class:`Fold` and :py:class:`Unnest`.
    It takes a nested value in some format and expands it, but it assumes the value is ragged
    (e.g., a variable length array or a record with variant schemas).

    To adapt the ragged structure to a fixed schema, it produces two columns: The *tags* and the *values*.
    Each input row then generates one row per entry from the nested value.
    Because the schema is variable, both columns will be strings
    and later transforms can sort out the data typing.
    To avoid losing data, empty records will produce one row with empty strings for the outputs.

    For arrays (JSON arrays, Markdown rows or csv rows), the tags are the numeric indices;
    for structured records, the tags are the record keys.

    .. py:attribute:: pipeline
        :type: Transform

        The input pipeline (required).

    .. py:attribute:: inputs
        :type: tuple(str)

        The list of columns to be folded.
        They will be dropped from the output, so use :py:class:`Copy` to preserve them.

    .. py:attribute:: tags
        :type: str

        The output column receiving the record keys or the (0-based) array indices.
        It cannot overwrite existing columns, so use :py:class:`Drop` to remove unwanted columns.

    .. py:attribute:: values
        :type: str

        The output column receiving the record values or the array entries.
        It cannot overwrite existing columns, so use :py:class:`Drop` to remove unwanted columns.

    .. py:attribute:: format
        :type: str

        The format of the nested record or array. Supported nesting formats are:

        * ``csv`` Comma-separated values treated as an array.
        * ``json``, ``jsonl`` JavaScript Object Notation records or arrays (``{..}`` or ``[...]``)
        * ``md`` GitHub Markdown row values treated as an array
        * ``text`` Single text field treated as an array with one text value.

    .. py:attribute:: config
        :type: kwargs

        Configuration parameters that will be passed to the unnesting format reader.

Usage
^^^^^

.. code-block:: python

   Iterate(p, 'Ragged', 'Index', 'Value', 'csv')
   Iterate(p, 'Variant', 'Key', 'Value', 'jsonl')
