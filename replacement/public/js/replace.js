frappe.ui.form.on('Replacement', {
    before_save: function(frm) {
        // Check if the document is new
        if (frm.doc.__islocal) {
            frappe.call({
                method: 'replacement.replacement.test.create_reverse_replacement_doc',
                args: {
                    item: frm.doc.item,
                    replacement_item: frm.doc.replacement_item
                },
                callback: function(r) {
                    if (!r.exc) {
                        
                    }
                }
            });
        }
    }
});
