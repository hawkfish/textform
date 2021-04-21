Layouts
=======

.. py:currentmodule:: textform.layouts

Layouts are classes for handling record string layouts.
:py:mod:`textform` uses these layouts to convert between strings in various layouts and records.

Each layout has up to four string converters.
There are readers and writers, each of which has a variant for individual strings or entire files.

.. py:function:: ReaderFactory(name, layout, iterable, **config)

    Constructs a :py:class:`LineReader` for the given ``layout``.
    The reader will parse each string into a string tuple.

    :param str name: The name of the calling transform.
    :param str layout: The string layout to read.
    :param iterable: The source of the strings to parse.
    :param config: Optional configuration parameters for the :py:class:`LineReader`.
    :return: An :py:obj:`iterable` that generates parsed tuples of values
    :raises TransformException: if the layout is unknown or the *iterable* is not :py:obj:`iterable`.


.. py:function:: DictReaderFactory(name, layout, iterable, fieldnames, **config)

    Constructs a :py:class:`DictReader` for the given ``layout``.
    The reader will parse each string into a record.

    :type fields: str or tuple(str)
    :param str name: The name of the calling transform.
    :param str layout: The string layout to read.
    :param iterable: The source of the strings to parse.
    :param fields fieldnames: The fields to read from the record.
    :param config: Optional configuration parameters for the :py:class:`DictReader`.
    :return: An :py:obj:`iterable` that generates parsed records
    :raises TransformException: if the layout is unknown or the *iterable* is not :py:obj:`iterable`.

.. py:function:: WriterFactory(name, layout, outfile, fieldnames, **config)

    Constructs a :py:obj:`DictWriter` for the given ``layout`` that converts
    :py:obj:`tuple`\ s into strings in the given layout and writes them to the output.

    :type fields: str or tuple(str)
    :param str name: The name of the calling transform.
    :param str layout: The string layout to write.
    :param outfile: The destination for the strings.
    :param fields fieldnames: The fields corresponding to the :py:obj:`tuple` values.
    :param config: Optional configuration parameters for the :py:class`DictReader`.
    :return: :py:class:`LineWriter` that writes layoutted :py:obj:`tuple`\ s
    :raises TransformException: if the layout is unknown or the *outfile* does not have a :py:meth:`write` method

.. py:function:: DictWriterFactory(name, layout, outfile, fieldnames, **config)

    Constructs a :py:class:`DictWriter` for the given ``layout`` that converts
    :py:obj:`dict`\ s into strings in the given layout and writes them to the output.

    :type fields: str or tuple(str)
    :param str name: The name of the calling transform.
    :param str layout: The string layout to write.
    :param writable outfile: The destination for the strings.
    :param fields fieldnames: The fields corresponding to the tuple values.
    :param config: Optional configuration parameters for the :py:class:`DictReader`.
    :return: A :py:class:`DictWriter` that writes layoutted tuples
    :raises TransformException: if the layout is unknown or the *outfile* does not have a :py:meth:`write` method

.. toctree::
   :maxdepth: 2
   :caption: Formats:

   csv
   json
   jsonl
   md
   rst
   text
