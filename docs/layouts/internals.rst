Internal layout objects
=======================

.. py:currentmodule:: txf.layouts

These classes are designed to be used by layout implementors.

.. py:class:: DictReader(iterable[, fieldnames=None[, **config]])

    A base record iterator class.

    .. py:attribute:: fieldnames

        A tuple of the field names in the fixed schema being iterated over.
        If the field names were not specified in the constructor,
        then it will read them from the first row.
        If the row is a dictionary, the field names are extracted and the row itself is buffered.
        If the row is a tuple, it is presumed to contain the field names.
        If the row is a single value, that value is the single field name.
        If the :py:obj:`iterable` is empty,
        the field names are taken from the ``default_fieldnames`` member of the ``config``.

    .. py:attribute:: line_num

        The current line number.

    .. py:method:: next()

        Reads the next set of values from the input iterator.
        If the values are a :py:obj:`dict`,
        the record is updated with the contents of the dictionary.
        If the values are a :py:obj:`tuple`,
        the record is constructed from the values and the ordered field names.
        Otherwise, the values are returned as the value for every field name.
        Missing field names are set to ``None``.

.. py:class:: BufferedAppend()

    Constructs an :py:obj:`iterator` that can buffer appends for iteration.

    .. py:method:: append(value)

        Buffers the value for a call to :py:func:`next`.
        Multiple calls overwrite the value.

    .. py:method:: next()

        Returns the buffered value, or raises :py:exc:`StopIteration` if nothing is buffered.

.. py:class:: BufferedWrite()

    Constructs an :py:obj:`iterator` that can buffer writes for iteration.

    .. py:method:: write(string)

        Buffers the string for a call to :py:func:`next`.
        Multiple calls append to the existing string.

    .. py:method:: next()

        Returns the buffered string, or raises :py:exc:`StopIteration` if nothing is buffered.

