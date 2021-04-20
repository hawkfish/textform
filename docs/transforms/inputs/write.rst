Write: export formatted records to a writable object
====================================================

.. py:currentmodule:: textform

.. py:class:: Write(source, outfile[, format='csv'[, **config]])

    The ``Write`` transform writes records to a stream using a specified format.
    It has no impact on the stream except to write the records as they come in.
    ``Write`` is the logical inverse of :py:class:`Read`.

    .. py:attribute:: source
        :type: Transform

    .. py:attribute:: outfile
        :type: writable

        The stream where the data will be sent.

    .. py:attribute:: format
        :type: writable

        The format to generate the output in.

        Supported writing formats are:

        * ``csv`` Comma-Separated Values
        * ``json`` JavaScript Object Notation (an array of objects)
        * ``jsonl`` JavaScript Object Notation lines (one object per row)
        * ``md`` GitHub Markdown
        * ``py`` Python *dict*\ s
        * ``rst`` CSV format escaped for reStructured text

    .. py:attribute:: config
        :type: kwargs

        Extra arguments to be passed to the formatting object.


Usage
^^^^^

.. code-block:: python

   Write(p, sys.stdout)
   Write(p, open("log.json", "w"), 'jsonl')
