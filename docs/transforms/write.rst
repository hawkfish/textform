Write
=====

The ``Write`` transform writes records to a stream using a specified format.
It has no impact on the stream except to write the records as they come in.
Its arguments are:

* *pipeline* The input pipeline (required).
* *outfile* The writeable stream where the data will be sent.
* *format* The format to generate the output in. Default: ``'csv'``.
* *\ *\ *config* Extra arguments to be passed to the formatting object.

``Write`` is the logical inverse of ``Read``.

Formats:
^^^^^^^^
Supported writing formats are:

* ``csv`` Comma-Separated Values
* ``json`` JavaScript Object Notation (an array of objects)
* ``jsonl`` JavaScript Object Notation lines (one object per row)
* ``md`` GitHub Markdown
* ``py`` Python *dict*\ s

Examples:
^^^^^^^^^

.. code-block:: python

   Write(p, sys.stdout)
   Write(p, sys.stderr, 'jsonl')
