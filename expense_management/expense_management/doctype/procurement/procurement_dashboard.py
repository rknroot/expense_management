from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'fieldname': 'request_id',
		'transactions': [
			{
				'label': _('Quote'),
				'items': ['Quote']
			},
		]
	}