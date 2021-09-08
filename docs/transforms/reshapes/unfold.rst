Unfold: Rotate one field to many
================================

.. py:currentmodule:: txf

.. py:class:: Unfold(source, inputs, outputs)

    The ``Unfold`` transform unfolds (pivots) a set of fields.
    Simple unfolding consists of rotating a single input field into multiple output fields.

    This can be generalised to multiple input fields where the output fields are broken up into equal-sized *groups*,
    and each group is generated from one of the input fields.
    ``Unfold`` is the inverse of :py:class:`Fold`.

    .. py:attribute:: source
        :type: Transform

        The input pipeline.

    .. py:attribute:: inputs
        :type: tuple(str)

        The list of fields to be unfolded.
        They will be dropped from the output, so use :py:class:`Copy` to preserve them.
        The first field is the *tag* field and is used to identify wich element of the group the row belongs to.
        Each subsequent input field contains the values for an entire group.

    .. py:attribute:: outputs
        :type: tuple(str)

        The output fields receiving the unfolded input fields.
        The output fields are broken into equal-sized groups, one per input field.
        The number of *inputs* must be an even multiple of the number of *outputs*.
        They cannot overwrite existing fields, so use :py:class:`Drop` to remove unwanted fields.

    .. py:attribute:: tags
        :type: dict(any,int)

        The optional mapping from tag values to group positions.
        If not provided, it will be generated sequentially from the values in the first record.

    ``Unfold`` can rotate data where the output rows are generated from non-consecutive input rows.
    To identify output rows, the remaining fields (called the *fixed* fields) are used as a key
    for accumulating the values of a row.
    When a row is complete, it is output.

    Because the rows for an output field can appear at any point,
    the *tags* are used to assign fields to output columns.
    The first time a tag is seen, it is assigned to the next group position,
    so the order of the tags in the first record must match the layout of the groups.

Usage
^^^^^

.. code-block:: python

   Unfold(p, ('Year', 'Sales',),
             ('Sales 1992', 'Sales 1993', 'Sales 1994',))
   Unfold(p, ('Year', 'Sales', 'Profit',),
             ('Sales 1992', 'Sales 1993', 'Sales 1994',
              'Profit 1992', 'Profit 1993', 'Profit 1994',))

Examples
^^^^^^^^

Single Group
------------

The first Usage example is a case where a single measure (Sales) has been tagged by Year,
so that each Sales value is in a separate row:

.. csv-table:: Input
    :header: "Dept", "Year", "Sales"
    :align: left

    Home, 1992, "S-H-1992"
    Home, 1993, "S-H-1993"
    Home, 1994, "S-H-1994"
    Auto, 1992, "S-A-1992"
    Auto, 1993, "S-A-1993"
    Auto, 1994, "S-A-1994"

In order to have all the Sales values for a Dept in a single record,
the table needs to have all the Sales for that Dept rotated into the same row.
``Unfold`` takes the tags and the field containing the values as its inputs
and the fields to rotate them to them in as the outputs.

The first *input* field is the "Tags" field, which contains the value used to
identify the original row.
In this example, this is the Year of the field.
This tag is used to track which group field an input row belongs to.
The tags are tracked in order, and they must have the same number as the inputs.

After Unfolding, each Sales value appears in a separate field, with the Year in the field name:

.. csv-table:: Output
    :header: "Dept", "Sales 1992", "Sales 1993", "Sales 1994"
    :align: left

    Home, "S-H-1992", "S-H-1993", "S-H-1994"
    Auto, "S-A-1992", "S-A-1993", "S-A-1994"

Multiple Groups
---------------

The second Usage example is a related case where multiple measures (Sales and Profit)
have been tagged by Year so that the Sales and Profits for each Year are in separate fields.

.. csv-table:: Input
    :header: "Dept", "Year", "Sales", "Profit"
    :align: left

    Home, 1992, "S-H-1992", "P-H-1992"
    Home, 1993, "S-H-1993", "P-H-1993"
    Home, 1994, "S-H-1994", "P-H-1994"
    Auto, 1992, "S-A-1992", "P-A-1992"
    Auto, 1993, "S-A-1993", "P-A-1993"
    Auto, 1994, "S-A-1994", "P-A-1994"

In order to have all the Sales and Profit values for a Dept in a single record,
the table needs to have all the Sales and Profit values for that Dept rotated into the same row.
This means that there are two groups that need to be Unfolded: Sales and Profit,
and the value from each group needs to be rotated into the appropriate group field.

To express this, each group is listed in order in the *outputs*
and the *inputs* are mapped to the corresponding *tag* value and *output* field.
In this example, the Year is again the first *output* field,
and the following *output* fields are the groups in the order given by the *inputs*.

After Unfolding, each Sales and Profit value appears in a separate field:

.. csv-table:: Output
    :header: "Dept", "Sales 1992", "Sales 1993", "Sales 1994", "Profit 1992", "Profit 1993", "Profit 1994"
    :align: left
    :widths: 1, 8, 8, 8, 8, 8, 8

    Home, "S-H-1992", "S-H-1993", "S-H-1994", "P-H-1992", "P-H-1993", "P-H-1994"
    Auto, "S-A-1992", "S-A-1993", "S-A-1994", "P-A-1992", "P-A-1993", "P-A-1994"

Interleaved Records
-------------------

Another powerful use case for ``Unfold`` is to assemble records that may be interleaved.
In this example, the values of two fields appear mixed in the file, but identified by output Row and Column:

.. csv-table:: Input
    :header: "Row", "Column", "Data"
    :align: left

    0,0,"#BLENDs"
    1,0,5
    2,0,6
    3,0,7
    4,0,8
    5,0,9
    6,0,10
    7,0,"Total"
    0,1,"#Queries"
    1,1,1
    2,1,11
    3,1,85
    4,1,449
    5,1,1511
    6,1,9216
    7,1,11273

To assemble the rows, we Unfold the Data column into a single group,
using the Column field as the tags to identify the group field:

.. code-block:: python

   Unfold(p, ('Column', 'Data',), ('BLENDs', '#Queries',),
                                  {'BLENDs': 0, '#Queries': 1})

The result is a table containing the eight interleaved fields reassembled using the tags to identify the output group:

.. csv-table:: Input
    :header: "Row", "#BLENDs", "#Queries"
    :align: left

    0,#BLENDs,#Queries
    1,5,1
    2,6,11
    3,7,85
    4,8,449
    5,9,1511
    6,10,9216
    7,Total,11273
