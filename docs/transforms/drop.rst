Drop
====

The ``Drop`` transform removes columns from the records. Its arguments are:

* *pipeline* The input pipeline (required).
* *inputs* The name(s) of the columns to remove.

Examples:
^^^^^^^^^

.. code-block:: python
  
   Drop(p, 'Invalid')
