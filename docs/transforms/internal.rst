Internals
=========

.. py:currentmodule:: txf

.. py:class:: Transform(name[, inputs=()[, outputs=()[, source=None]]])

    The base class for all transforms.
    It provides services for creating and validating the common attributes.
    It is an :py:obj:`iterable`, so it can be used in ``for`` loops.

    .. py:attribute:: source
        :type: Transform or None

        The input pipeline.

    .. py:attribute:: inputs
        :type: tuple(str)

        The input field names, if any.

    .. py:attribute:: input
        :type: str

        If there is only one input, :py:attr:`input` is set to it.

    .. py:attribute:: outputs
        :type: tuple(str)

        The output field names, if any.

    .. py:attribute:: output
        :type: str

        If there is only one output, :py:attr:`output` is set to it.

    .. py:attribute:: fieldnames
        :type: tuple(str)

        The full list of fields a record will have after being processed by this transform.
        It is carefully maintained to preserve physical layout order, e.g., a :py:class:`Split`
        transformation will replace the input in the source :py:attr:`fieldnames` with
        the outputs.

    .. py:attribute:: schema
        :type: dict(str -> metadata)

        A mapping from field names to metadata.

    .. py:method getSchemaType(field)

        Returns the Python type object of the field.

    .. py:method:: updateSchemaType(field[, ftype = None])

        Sets the Python type object of the field.
        Used by transforms like :py:class:`Text` that know the data type of a field at construction time.


    .. py:method readrow()

        Returns the next row.

    .. py:method pump()

        Reads all the rows and returns the count.

.. py:exception:: TransformException(message=None)

    A module-specific exception derived from :py:exc:`Exception`

