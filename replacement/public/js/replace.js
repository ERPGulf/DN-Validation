frappe.ui.form.on('Replacement', {
    before_save: function(frm) {
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
frappe.listview_settings['Replacement'] = {
    onload: function(listview) {
        listview.page.add_inner_button(__('Search Item'), function() {
            frappe.prompt([
                {
                    'fieldname': 'item',
                    'fieldtype': 'Link',
                    'label': __('Item'),
                    'options': 'Item',
                    'reqd': 1,
                },
            ], function(values){
                frappe.call({
                    method: 'replacement.replacement.test2.search_items_and_replacements', // Adjust the method path
                    args: {
                        item_name: values.item,
                    },
                    callback: function(r) {
                        if (!r.exc) {
                            var message = '<b>Items:</b> ' + r.message.items.join(', ') + '<br><b>Replacements:</b> ' + r.message.replacements.join(', ');
                            frappe.msgprint(message);
                            listview.refresh();
                        }
                    }
                });
            }, 'Search Item', 'View');
        });
    }
};

