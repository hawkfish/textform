Nest
=====

The ``Nest`` transform combines columns into a single field using a particular format. Its arguments are:

* *pipeline* The input pipeline (required).
* *inputs* The columns to combine. They will be dropped from the output, so use ``Copy`` to preserve them.
* *output* The output column receiving the merged values.
* *format* The format to generate the output in. Default: ``'csv'``.
* *\ *\ *config* Extra arguments to be passed to the formatting object.

``Nest`` is the logical inverse of ``Unnest``.

Formats:
^^^^^^^^
Supported nesting formats are:

* ``csv`` Comma-separated string
* ``json``, ``jsonl`` JavaScript Object Notation string
* ``md`` GitHub Markdown
* ``py`` Python *dict*

Examples:
^^^^^^^^^

.. code-block:: python
  
   Nest(p, ('F1', 'F2',) 'CSV', 'csv')
   Nest(p, ('Sales 1992', 'Sales 1993',) 'Dict', 'py')
