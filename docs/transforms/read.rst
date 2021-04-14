Read
=====

The ``Read`` transform pulls records from an ``iterable`` using a particular format. Its arguments are:

* *iterable* The input. Each row will be generated from the result ``next(iterable)``.
* *pipeline* An optional input pipeline. New rows will be merged with the output of this pipeline.
* *format* The format to generate the output in. Default: ``'csv'``.
* *\ *\ *config* Extra arguments to be passed to the formatting object.

``Read`` is the logical inverse of ``Write``.

Formats:
^^^^^^^^
Supported nesting formats are:

* ``csv`` Comma-separated values. The header will be read to provide the column names.
* ``json`` JavaScript Object Notation records in array format (``[{..},...]``)
* ``jsonl`` JavaScript Object Notation Line format (``{...}\n{...}\n...``)
* ``md`` GitHub Markdown tables with headers
* ``py`` Python *dict* stream
* ``text`` Treats the file as a single column with a name taken from ``config['default_fieldnames']``.

Examples:
^^^^^^^^^

.. code-block:: python

   Read(p, sys.stdin 'csv')
   Read(p, records, 'py')
