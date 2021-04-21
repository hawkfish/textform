Write: Export records to a writable object using a layout
=========================================================

.. py:currentmodule:: textform

.. py:class:: Write(source, outfile[, layout='csv'[, **config]])

    The ``Write`` transform writes records to a stream using a specified layout.
    It has no impact on the stream except to write the records as they come in.
    ``Write`` is the logical inverse of :py:class:`Read`.

    .. py:attribute:: source
        :type: Transform

    .. py:attribute:: outfile
        :type: writable

        The stream where the data will be sent.

    .. py:attribute:: layout
        :type: writable

        The layout to use for the output.

        Supported write layouts are:

        * ``csv`` Comma-Separated Values
        * ``json`` JavaScript Object Notation (an array of objects)
        * ``jsonl`` JavaScript Object Notation lines (one object per row)
        * ``md`` GitHub Markdown
        * ``py`` Python *dict*\ s
        * ``rst`` csv escaped for reStructured text

    .. py:attribute:: config
        :type: kwargs

        Extra arguments to be passed to the layout object.


Usage
^^^^^

.. code-block:: python

   Write(p, sys.stdout)
   Write(p, open("log.json", "w"), 'jsonl')
