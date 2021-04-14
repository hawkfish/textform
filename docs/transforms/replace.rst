Replace
=======

The ``Replace`` uses a regular expresssion to reformat a column using capture groups. Its arguments are:

* *pipeline* The input pipeline (required).
* *input* The name of the string column to apply the *pattern* to. It will be replaced, so use ``Copy`` to preserve the original.
* *search* A regular expression with capture groups that can be referenced in the *replace* string.
  If the pattern does not match, the value is unchanged.
* *replace* An expansion string with references to capture groups. 

``Replace`` is a special case of ``Format``.

Examples:
^^^^^^^^^

.. code-block:: python

   Replace(p, 'US Date', '(d+)/(d+)/(d+)', '\3-\2-\1')
