Unnest
======

.. py:class:: Unnest(pipeline, input, outputs, format='csv', **config)

    The ``Unnest`` transform extracts one level of a nested record stored as a string in some format.
    ``Unnest`` is the logical inverse of :py:class:`Nest`.

.. py:attribute:: pipeline
    :type: Transform
    :noindex:

    The input pipeline (required).

.. py:attribute:: input
    :type: str
    :noindex:

    The column to unnest.
    It will be dropped from the schema, so use :py:class:`Copy` to preserve it.

.. py:attribute:: outputs
    :type: tuple(str)
    :noindex:

    The output columns to be extracted. Only the listed fields will be extracted.

.. py:attribute:: format
    :type: str
    :noindex:

    The format of the input string. Supported nesting formats are:

    * ``csv`` Comma-separated values. The *outputs* will be used to provide the column names.
    * ``json``, ``jsonl`` JavaScript Object Notation records (``{..}``). Only keys from *outputs* will be returned
    * ``md`` GitHub Markdown rows. The *outputs* will be used to provide the column names.
    * ``text`` Treats the column as an array with one text value tagged with the first output name.

.. py:attribute:: config
    :type: kwargs
    :noindex:

    Configuration parameters that will be passed to the unnesting reader.

Examples:
^^^^^^^^^

.. code-block:: python

   Unnest(p, 'CSV', ('F1', 'F2',), 'csv')
   Unnest(p, 'Dict', ('Sales 1992', 'Sales 1993',), 'py')
