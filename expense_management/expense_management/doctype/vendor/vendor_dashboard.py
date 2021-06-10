from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'fieldname': 'vendor',
		'transactions': [
			{
				'label': _('Quote'),
				'items': ['Quote']
			},
		]
	}