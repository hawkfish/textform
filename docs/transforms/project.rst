Project
=======

The ``Project`` transform computes (projects) a new column using an arbitrary function of zero or more input columns. Its arguments are:

* *pipeline* The input pipeline (required).
* *inputs* The columns to combine. They will *not* be dropped from the output.
* *function* A *callable* implementing the function.
  It will be given the values of *inputs* as positional arguments **in the given order**.

Examples:
^^^^^^^^^

.. code-block:: python
  
   Project(p, 'Number', 'Square', lambda x: x*x)
   Project(p, () 'Roll', rand.randint(1,6))
