frappe.ui.form.on('Delivery Note', {
    onload: function (frm) {
        // Custom button to create Sales Return
        if (frm.doc.status !== 'Closed') {
            frm.add_custom_button(__('Sales Return'), function () {
                frappe.call({
                    method: 'replacement.replacement.delivery.validate_returned_quantity',
                    args: {
                        doc_name: frm.doc.name,
                    },
                    callback: function (r) {
                        var differences = r.message;

                        // Check if any difference is zero
                        var hasZeroDifference = Object.values(differences).some(function (diff) {
                            return diff === 0;
                        });

                        if (hasZeroDifference) {
                            // Set the document status to 'Closed'
                            frm.set_value('status', 'Closed');
                            frappe.throw(__('Sales Return cannot be created for already completed delivery note {0}. Document status set to Closed.', [frm.doc.name]));
                        } else {
                            // Call the original function for creating Sales Return
                            createSalesReturn(frm);
                        }
                    }
                });
            }, __("Create"));
        }
    },
});

// Function to display differences for each item
function displayItemDifferences(frm, differences) {
    // Iterate through each item and display the difference
    for (var item_name in differences) {
        var difference = differences[item_name];
        frappe.msgprint(__('Item: {0}, Difference: {1}', [item_name, difference]));
    }
}

// Original function for creating Sales Return
function createSalesReturn(frm) {
    frappe.model.open_mapped_doc({
        method: "erpnext.stock.doctype.delivery_note.delivery_note.make_sales_return",
        frm: frm
    });
}
