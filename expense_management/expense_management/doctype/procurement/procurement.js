// Copyright (c) 2021, Eco Data and contributors
// For license information, please see license.txt
//cur_frm.add_fetch('contact', 'email_id', 'email_id')
frappe.ui.form.on('Procurement', {
	setup: function(frm) {
		frm.custom_make_buttons = {
			'Supplier Quotation': 'Create'
		}
	},
	onload(frm){
		if(!frm.doc.__islocal){
		frappe.call({
			method : "frappe.client.get_list",
			args:{
				"doctype" : "Quote",
				filters:{
					"request_id" : frm.doc.name
				},
				fields:["name","request_id"]
			},
			callback(r){
				frm.clear_table("quote_table")
				$.each(r.message,function(i,d){
					frappe.db.get_doc('Quote',d.name)
					.then(r => {
						var row = frappe.model.add_child(frm.doc, "Quote Table", "quote_table");
						row.quote = r.name;
					})
				})
				refresh_field("quote_table");
				cur_frm.save();
			}
		})
		}
	},
	refresh: function(frm) {
		frm.add_custom_button(__('Sent Mail'),
			function(frm) {
					//console.log(frm.doc.name);
					frappe.call({
						method: "expense_management.expense_management.doctype.procurement.procurement.mail_notification",
									args: { "docid":cur_frm.doc.name
										},
									callback: function(r){
										cur_frm.reload_doc();
									}
								});


							})

	}
});
frappe.ui.form.on('Vendors', {
	before_vendor_remove:function(frm,cdt,cdn){
						var deleted_row = frappe.get_doc(cdt, cdn);
						if ((deleted_row.send_mail == 1) && (!deleted_row.__islocal)) {
							frappe.msgprint('You do not have permissions to delete a row. Reload to proceed.');
                                cur_frm.reload_doc();
                                throw 'err';
                                cur_frm.refresh_fields();
						}		
                     },

});
