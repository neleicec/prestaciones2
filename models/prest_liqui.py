#  -*- coding: utf-8 -*- 

from odoo import models, fields, api
from datetime import date, datetime, time
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
	fecha_actual = fields.Date(string='Fecha Actual', required=True,
        default=lambda self: fields.Date.to_string(date.today()),
		readonly=True)

	@api.multi
	@api.depends('name')
	def _totaltotal(self):
		for record in self:
			sumador_anual = 0.0
			sumador_interes = 0.0
			gs = self.env['prest'].search([])
			for j in gs:
				if j.name == record.name:
					sumador_anual = j.acumulado_al_ano
					sumador_interes = sumador_interes + j.interes_trimestral
			record.total_pagar_anos_servicios = sumador_anual
			record.total_intereses = sumador_interes

	total_pagar_anos_servicios = fields.Float(
		string='Record Acumulado',
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
				record.doblete = record.total_pagar_anos_servicios * 1
			else:
				record.doblete = 0.0
	contiene_doblete = fields.Boolean(
		string= 'Contiene Doblete',
		store = True)
	
	
	@api.depends('name','contiene_doblete')
	def _totalfinal (self):
		for record in self:
			if record.contiene_doblete == False:
				record.total_liquidar = (record.total_pagar_anos_servicios)-(record.anticipo_acumulado)
			else:
				record.total_liquidar = (record.total_pagar_anos_servicios + record.doblete)-(record.anticipo_acumulado)
	total_liquidar = fields.Float(
		string= 'Total a Liquidar',
		compute = '_totalfinal',
		store = True)
	doblete = fields.Float(
		string = 'Doblete',
		compute = '_doble',
		store = True)
	

	@api.multi
	@api.depends('name')
	def _prueba(self):
		for record in self:
			sumador_anticipo = 0.0
			gs = self.env['anticipo'].search([])
			for j in gs:
				if j.name == record.name:
					sumador_anticipo = j.monto_anticipo + sumador_anticipo
			record.anticipo_acumulado = sumador_anticipo

	anticipo_acumulado = fields.Float(
		string='Anticipo Acumulado',
		compute='_prueba',
		store=True)

	elegir_metodo = fields.Selection( 
        string='Elegir Metodo',
        selection=[('metodo1','Metodo 1'),('metodo2','Metodo 2')],
        required=True,
		help= "Elegir el metodo de mayor cantidad")
	