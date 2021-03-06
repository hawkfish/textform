Iterate: Expand ragged records into multiple rows
=================================================

.. py:currentmodule:: txf

.. py:class:: Iterate(pipeline, input, tags, values[, layout='csv'[, **config]])

    The ``Iterate`` transform is a cross between :py:class:`Fold` and :py:class:`Unnest`.
    It takes a nested value in some layout and expands it, but it assumes the value is ragged
    (e.g., a variable length array or a record with variant schemas).

    To adapt the ragged structure to a fixed schema, it produces two fields: The *tags* and the *values*.
    Each input row then generates one row per entry from the nested value.
    Because the schema is variable, both fields will be strings
    and later transforms can sort out the data typing.
    To avoid losing data, empty records will produce one row with empty strings for the outputs.

    For arrays (JSON arrays, Markdown rows or csv rows), the tags are the numeric indices;
    for structured records, the tags are the record keys.

    .. py:attribute:: pipeline
        :type: Transform

        The input pipeline (required).

    .. py:attribute:: inputs
        :type: tuple(str)

        The list of fields to be folded.
        They will be dropped from the output, so use :py:class:`Copy` to preserve them.

    .. py:attribute:: tags
        :type: str

        The output field receiving the record keys or the (0-based) array indices.
        It cannot overwrite existing fields, so use :py:class:`Drop` to remove unwanted fields.

    .. py:attribute:: values
        :type: str

        The output field receiving the record values or the array entries.
        It cannot overwrite existing fields, so use :py:class:`Drop` to remove unwanted fields.

    .. py:attribute:: layout
        :type: str

        The layout of the nested record or array. Supported nesting layouts are:

        * ``csv`` Comma-separated values treated as an array.
        * ``json``, ``jsonl`` JavaScript Object Notation records or arrays (``{..}`` or ``[...]``)
        * ``md`` GitHub Markdown row values treated as an array
        * ``text`` Single text field treated as an array with one text value.

    .. py:attribute:: config
        :type: kwargs

        Configuration parameters that will be passed to the unnesting layout reader.

Usage
^^^^^

.. code-block:: python

   Iterate(p, 'Ragged', 'Index', 'Value', 'csv')
   Iterate(p, 'Variant', 'Key', 'Value', 'jsonl')
