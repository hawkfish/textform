Formats
=======

.. py:currentmodule:: textform.formats

Formats are classes for handling record string layouts.
:py:module`textform` uses these formats to convert between strings in various formats and records.

Each format has up to four string converters.
There are readers and writers, each of which has a variant for individual strings or entire files.

.. py:function:: ReaderFactory(name, format, iterable, **config)

    Constructs a :py:class:`LineReader` for the given ``format``.
    The reader will parse each string into a string tuple.

    :param str name: The name of the calling transform.
    :param str format: The string format to read.
    :param iterable: The source of the strings to parse.
    :param config: Optional configuration parameters for the :py:class:`LineReader`.
    :return: An :py:obj:`iterable` that generates parsed tuples of values
    :raises TransformException: if the format is unknown or the *iterable* is not :py:obj:`iterable`.


.. py:function:: DictReaderFactory(name, format, iterable, fieldnames, **config)

    Constructs a :py:class:`DictReader` for the given ``format``.
    The reader will parse each string into a record.

    :type fields: str or tuple(str)
    :param str name: The name of the calling transform.
    :param str format: The string format to read.
    :param iterable: The source of the strings to parse.
    :param fields fieldnames: The fields to read from the record.
    :param config: Optional configuration parameters for the :py:class:`DictReader`.
    :return: An :py:obj:`iterable` that generates parsed records
    :raises TransformException: if the format is unknown or the *iterable* is not :py:obj:`iterable`.

.. py:function:: WriterFactory(name, format, outfile, fieldnames, **config)

    Constructs a :py:obj:`DictWriter` for the given ``format`` that converts
    :py:obj:`tuple`\ s into strings in the given format and writes them to the output.

    :type fields: str or tuple(str)
    :param str name: The name of the calling transform.
    :param str format: The string format to write.
    :param outfile: The destination for the strings.
    :param fields fieldnames: The fields corresponding to the :py:obj:`tuple` values.
    :param config: Optional configuration parameters for the :py:class`DictReader`.
    :return: :py:class:`LineWriter` that writes formatted :py:obj:`tuple`\ s
    :raises TransformException: if the format is unknown or the *outfile* does not have a :py:meth:`write` method

.. py:function:: DictWriterFactory(name, format, outfile, fieldnames, **config)

    Constructs a :py:class:`DictWriter` for the given ``format`` that converts
    :py:obj:`dict`\ s into strings in the given format and writes them to the output.

    :type fields: str or tuple(str)
    :param str name: The name of the calling transform.
    :param str format: The string format to write.
    :param writable outfile: The destination for the strings.
    :param fields fieldnames: The fields corresponding to the tuple values.
    :param config: Optional configuration parameters for the :py:class:`DictReader`.
    :return: A :py:class:`DictWriter` that writes formatted tuples
    :raises TransformException: if the format is unknown or the *outfile* does not have a :py:meth:`write` method

.. toctree::
   :maxdepth: 2
   :caption: Formats:

   csv
   json
   jsonl
   md
   rst
   text
