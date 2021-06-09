# Copyright (c) 2021, Eco Data and contributors
# For license information, please see license.txt
# 
import frappe
from frappe.model.document import Document

class Procurement(Document):
	def validate(self):
		mail_notification = []
		for mail_id in self.get('vendor'):
			if mail_id.email in mail_notification:
				frappe.throw(("You Cannot Give {0} Multiple Times".format(mail_id.email)))
			else:
				mail_notification.append(mail_id.email)

		
@frappe.whitelist()
def mail_notification(docid):
			
			self = frappe.get_doc("Procurement",docid)
			u_email = []
			user = frappe.db.sql("""select email from `tabUser`""",as_dict=True)
			for user_email in user:
				u_email.append(user_email.email)

			for vendor in self.get("vendor"):
				#Creation on user if doesn't have 
				if vendor.email in u_email:
					pass
				else:
					user_record = frappe.new_doc("User")
					user_record.email = vendor.email
					user_record.first_name = vendor.vendor
					role_table = user_record.append('roles', {})
					role_table.role = "Expense Vendor"
					user_record.save(ignore_permissions = True)
				if vendor.send_mail == 0:
					#Mail notification should be send corresponding vendor
					subj = 'Procurement Quote Notification - ' + self.name
					notification_message = 'Hello, \n Procurement Quotation was sent. Use the link to fill Quote - <a href="quote" target="_blank">{1}</a> \
					.'.format(self.name, self.name)	
					frappe.sendmail(vendor.email,subject=subj,\
					message = notification_message)
				#Creation of quote while click on send mail button
					quote_record = frappe.new_doc("Quote")
					quote_record.request_id = self.name
					quote_record.email = vendor.email
					vendor.send_mail = "1"
					quote_record.insert(ignore_permissions = True)
					ignore_permissions = False
					quote_record.save(ignore_permissions = True)
				#Quote id sholud be update in procurement quote table on creation of quote 	
					q_table = self.append('quote_table', {})
					q_table.quote = quote_record.name
					self.save()
			frappe.msgprint('Procurement Notification has been sent')


# User Permission 
@frappe.whitelist()
def get_permissions(user):
	retval = ''
	if "System Manager" in frappe.permissions.get_roles(frappe.session.user):
		pass

	elif "Expense Vendor" in frappe.permissions.get_roles(frappe.session.user):
		retval = """((`tabQuote`.email = '{user}' or 
				`tabQuote`.modified_by = '{user}'))""".format(user=frappe.session.user)

	return retval