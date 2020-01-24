# -*- coding: utf-8 -*- 
{
	'name': 'Prestaciones Sociales',
	'description': 'Este Modulo es sobre las Prestaciones Sociales en Venezuela',
	'author': 'PCN&RP Suministros y Servicios Generales C.A.',
	'depends': ['hr_payroll','hr_contract'],
	'application': True,
	'installable': True,
	'auto_install': False,
	'summary': 'Calcula las Prestaciones e imprime reporte',
	'version': '1.0',
	'license': 'LGPL-3',
	'category': 'Human Resources',
	'data': ['views/prest_view.xml','views/menu.xml','views/view_liqui.xml','views/report_anticipo.xml','views/report.xml','views/prestamo_view.xml','views/anticipo_view.xml'],
}