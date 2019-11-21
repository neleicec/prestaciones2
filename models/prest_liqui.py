#  -*- coding: utf-8 -*- 

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class presta(models.Model):
	_name='presta'
	# Barra de empleados
	name = fields.Many2one('hr.employee', 
		string='Empleado', 
		required=True)
	# Muestra la Fecha de Ingreso
	fecha_ingreso = fields.Date( 
		string='Fecha de Ingreso', 
		required=True,
		related="name.date_in",
		readonly=True)
	# Selecciona la Fecha Actual
	fecha_actual = fields.Date(
		string='Fecha Actual',
		required=True)

	@api.multi
	@api.depends('name')
	def _totaltotal(self):
		for record in self:
			sumador_anual = 0.0
			sumador_interes = 0.0
			gs = self.env['prest'].search([])
			for j in gs:
				if j.name == record.name:
					sumador_anual = sumador_anual + j.acumulado_al_ano
					sumador_interes = sumador_interes + j.interes_trimestral
			record.total_pagar_anos_servicios = sumador_anual
			record.total_intereses = sumador_interes

	total_pagar_anos_servicios = fields.Float(
		string='Total a pagar por los años',
		compute='_totaltotal',
		store=True)
	total_intereses = fields.Float(
		string="Total Intereses",
		compute="_totaltotal",
		store=True)

	@api.depends('contiene_doblete')
	def _doble(self):
		for record in self:
			if record.contiene_doblete == True:
				record.doblete = record.total_pagar_anos_servicios * 2
			else:
				record.doblete = 0.0
	contiene_doblete = fields.Boolean(
		string= 'Contiene Doblete',
		store = True)
	
	
	@api.depends('name','contiene_doblete')
	def _totalfinal (self):
		for record in self:
			if record.contiene_doblete == False:
				record.total_liquidar = record.total_pagar_anos_servicios + record.total_intereses 
			else:
				record.total_liquidar = record.total_pagar_anos_servicios + record.total_intereses + record.doblete
	total_liquidar = fields.Float(
		string= 'Total a Liquidar',
		compute = '_totalfinal',
		store = True)
	doblete = fields.Float(
		string = 'Doblete',
		compute = '_doble',
		store = True)
	