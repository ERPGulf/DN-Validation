frappe.ui.form.on('Delivery Note', {
    onload: function (frm) {
        // Add a custom button to the "Create" button's dropdown menu for "Sales Return"
        if (frm.doc.status !== 'Closed') {
            frm.add_custom_button(__('Sales Return'), function () {
                // Custom action before creating Sales Return
                frappe.call({
                    method: 'replacement.replacement.delivery.validate_returned_quantity',
                    args: {
                        doc_name: frm.doc.name
                    },
                    callback: function (r) {
                        if (!r.exc) {
                            // Check if the validation result is zero
                            if (r.message == 0) {
                                // Set status to 'Closed' for the current Delivery Note
                                frm.doc.status = 'Closed';
                                frm.doc.save();

                                frappe.throw(__("Sales Return cannot be created for already completed delivery note {0}.").format(frm.doc.name));
                                
                            } else if (r.message.difference !== 0) {
                                // Continue with Sales Return creation
                                makeSalesReturn(frm);
                            } else {
                                frappe.throw(__("Difference is zero. Sales Return cannot be created."));
                            }
                        }
                    }
                });
            }, __("Create"));
        }
    },

    refresh: function (frm) {
        if (frm.doc.docstatus == 1 && frm.doc.status !== 'Closed') {
            frm.add_custom_button(__('Sales Return'), function () {
                makeSalesReturn(frm);
            }, __('Create'));
        }
    }
});

function makeSalesReturn(frm) {
    frappe.model.open_mapped_doc({
        method: "erpnext.stock.doctype.delivery_note.delivery_note.make_sales_return",
        frm: frm
    });
    // Refresh the form to reflect the immediate status change
    frm.refresh();
}
