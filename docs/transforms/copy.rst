Copy
====

The ``Copy`` transform makes duplicates of a field. Its arguments are:

* *pipeline* The input pipeline (required).
* *input* The name of the field to duplicate. It will be not be removed.
* *outputs* One or more fields to receive the copies. 

Examples:
^^^^^^^^^

.. code-block:: python

   Copy(p, 'Year', 'Last Year')
   Copy(p, 'Original', ('Dupe 1', 'Dupe 2',))
