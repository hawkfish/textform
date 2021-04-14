Match
=====

The ``Match`` transform filters rows based on a regular expression. Its arguments are:

* *pipeline* The input pipeline (required).
* *input* The name of the column to apply the *pattern* to.
* *pattern* A regular expression to match against the *input*.
* *invert* Negative matching is difficult to specify with regular expressions, so this lets the caller reject rows that match a pattern. Default: ``False``.

``Match`` is a subclass of ``Select``.

Examples:
^^^^^^^^^

.. code-block:: python

   Match(p, 'Date', r'(\d+)/(\d+)/(\d+)') # Filter to valid dates
   Match(p, 'Line', '-----', True)        # Exclude formatting lines
