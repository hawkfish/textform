Text: Import lines as records from a text file
==============================================

.. py:currentmodule:: txf

.. py:class:: Text(iterable, output[, source=None])

    The ``Text`` transform pulls lines from an ``iterable`` in ``text`` format.
    ``Text`` is a subclass of :py:class:`Read`.

    .. py:attribute:: iterable
        :type: iterable

        The input. Each row will be generated from the result of ``next(iterable)``.

    .. py:attribute:: output
        :type: str

        The name of the output field containing the lines.

    .. py:attribute:: source
        :type: Transform or None

        An optional input pipeline. New rows will be merged with the output of this pipeline.

Usage
^^^^^

.. code-block:: python

   Text(sys.stdin, 'Line')
   Text(['Line 1', 'Line 2',], Sequence(None, 'Row #', 1))
