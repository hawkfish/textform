Unnest
======

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

* ``csv`` Comma-separated values. The *outputs* will be used to provide the column names.
* ``json``, ``jsonl`` JavaScript Object Notation records (``{..}``). Only keys from *outputs* will be returned
* ``md`` GitHub Markdown rows. The *outputs* will be used to provide the column names.
* ``text`` Treats the column as an array with one text value tagged with the first output name.

Examples:
^^^^^^^^^

.. code-block:: python

   Unnest(p, 'CSV', ('F1', 'F2',), 'csv')
   Unnest(p, 'Dict', ('Sales 1992', 'Sales 1993',), 'py')
