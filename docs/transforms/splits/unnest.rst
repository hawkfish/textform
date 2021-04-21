Unnest: Parse a string as a record using a layout
=================================================

.. py:currentmodule:: txf

.. py:class:: Unnest(pipeline, input, outputs, layout='csv', **config)

    The ``Unnest`` transform extracts one level of a nested record stored as a string in some layout.
    ``Unnest`` is the logical inverse of :py:class:`Nest`.

    .. py:attribute:: pipeline
        :type: Transform

        The input pipeline (required).

    .. py:attribute:: input
        :type: str

        The field to unnest.
        It will be dropped from the schema, so use :py:class:`Copy` to preserve it.

    .. py:attribute:: outputs
        :type: tuple(str)

        The output fields to be extracted. Only the listed fields will be extracted.
        They cannot overwrite existing fields. Use :py:class:`Drop` to remove unwanted fields.

    .. py:attribute:: layout
        :type: str

        The layout of the input string. Supported unnesting layouts are:

        * ``csv`` Comma-separated values. The *outputs* will be used to provide the field names.
        * ``json``, ``jsonl`` JavaScript Object Notation records (``{..}``). Only keys from *outputs* will be returned
        * ``md`` GitHub Markdown rows. The *outputs* will be used to provide the field names.
        * ``text`` Treats the field as an array with one text value tagged with the first output name.

    .. py:attribute:: config
        :type: kwargs

        Configuration parameters that will be passed to the unnesting reader.

Usage
^^^^^

.. code-block:: python

   Unnest(p, 'CSV', ('F1', 'F2',), 'csv')
   Unnest(p, 'Dict', ('Sales 1992', 'Sales 1993',), 'py')
