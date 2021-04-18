Replace
=======

.. py:currentmodule:: textform

.. py:class:: Replace(source, input, search, replace)

    The ``Replace`` transform uses a regular expresssion to reformat a column using capture groups.
    ``Replace`` is a subclass of :py:class:`Format`.

    .. py:attribute:: source
        :type: Transform

        The input pipeline.

    .. py:attribute:: input
        :type: str

        The name of the string column to apply the *pattern* to.
        The contents will be replaced, so use :py:class:`Copy` to preserve the original.

    .. py:attribute:: search
        :type: str

        A regular expression with capture groups that can be referenced in the *replace* string.
        If the pattern does not match, the value is unchanged.
        To avoid this, use :py:class:`Divide` with the same pattern to isolate the values that match.

    .. py:attribute:: replace
        :type: str

        An expansion string with references to capture groups, using Python's ``expand`` notation.

Usage
^^^^^

.. code-block:: python

   Replace(p, 'US Date', '(d+)/(d+)/(d+)', '\3-\2-\1')
