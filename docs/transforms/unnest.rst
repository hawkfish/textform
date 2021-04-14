Unnest
=====

The ``Unnest`` transform extracts one level of a nested record. Its arguments are:

* *pipeline* The input pipeline (required).
* *input* The column to unnest. It will be dropped from the output, so use ``Copy`` to preserve them.
* *outputs* The output columns to be extracted. Only the listed *outputs* will be extracted.
* *format* The format of the input. Default: ``'csv'``.
* *\ *\ *config* Extra arguments to be passed to the formatting object.

``Unnest`` is the logical inverse of ``Nest``.

Formats:
^^^^^^^^
Supported unnesting formats are:

* ``csv`` Comma-separated values. The header will be read to provide the column names.
* ``json`` JavaScript Object Notation records in array format (``[{..},...]``)
* ``jsonl`` JavaScript Object Notation Line format (``{...}\n{...}\n...``)
* ``md`` GitHub Markdown tables with headers
* ``py`` Python *dict* stream
* ``text`` Treats the column as a record with a single key taken from ``config['default_fieldnames']``.

Examples:
^^^^^^^^^

.. code-block:: python
  
   Unnest(p, 'CSV', ('F1', 'F2',), 'csv')
   Unnest(p, 'Dict', ('Sales 1992', 'Sales 1993',), 'py')
