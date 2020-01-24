#  -*- coding: utf-8 -*- 

from odoo import models, fields, api, exceptions
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
	def _acumuladoDiasAdicionales(self):
		for record in self:
				if record.name.id != False:
					self._cr.execute('SELECT acumulado_adicional FROM prest WHERE name = '+str(record.name.id)+' ORDER BY id DESC LIMIT 1')
					variable = self._cr.fetchall()
					record.acumuladoAdicional = float((variable[0])[0])
	acumuladoAdicional = fields.Float(
		string='Acumulado Adicional',
		compute='_acumuladoDiasAdicionales',
		store=True,
		default=1.0)
	
	@api.multi
	@api.depends('name')
	def _salarioIntegral(self):
		for record in self:
				if record.name.id != False:
					self._cr.execute('SELECT salario_integral FROM prest WHERE name = '+str(record.name.id)+' ORDER BY id DESC LIMIT 1')
					variable = self._cr.fetchall()
					record.salarioIntegral = float((variable[0])[0])

	salarioIntegral = fields.Float(
		string='Salario Integral',
		compute='_salarioIntegral',
		store=True,
		default=1.0)

	@api.multi
	@api.depends('name','elegir_metodo')
	def _anos_acumulados(self):
		for record in self:
				if record.name.id != False:
					self._cr.execute('SELECT acumulado_al_ano FROM prest WHERE name = '+str(record.name.id)+' ORDER BY id DESC LIMIT 1')
					variable = self._cr.fetchall()
					record.acumuladoPrestaciones = float((variable[0])[0])
	acumuladoPrestaciones = fields.Float(
		string='Record Acumulado',
		compute='_anos_acumulados',
		store=True,
		default=1.0)
	elegir_metodo = fields.Selection( 
        string='Elegir Metodo',
        selection=[('metodo1','Literal "a" y "b"'),('metodo2','Literal "c"')],
        required=True,
		help= "Elegir el metodo de mayor cantidad")
	
	@api.depends('contiene_doblete')
	def _doble(self):
		for record in self:
			if record.contiene_doblete == True:
				record.doblete = record.acumuladoPrestaciones * 1
			else:
				record.doblete = 0.0
	contiene_doblete = fields.Boolean(
		string= 'Contiene Doblete',
		store = True)
	
	@api.multi
	@api.depends('name','contiene_doblete','elegir_metodo')
	def _totalfinal (self):
		for record in self:
				if record.elegir_metodo == 'metodo1':
					if record.contiene_doblete == False:
						record.total_liquidar = (record.acumuladoPrestaciones + record.acumuladoAdicional)-(record.anticipo_acumulado)
					else:
						record.total_liquidar = (record.acumuladoPrestaciones + record.acumuladoAdicional + record.doblete)-(record.anticipo_acumulado)
				if record.elegir_metodo == 'metodo2':
					if record.contiene_doblete == False and record.name.years_service >= 1.0:
						years_service2 = float(record.name.years_service)
						record.total_liquidar = ((record.name.years_service * 30) * record.salarioIntegral)
					else:
						record.total_liquidar = ((record.name.years_service * 30 * record.salarioIntegral) + record.doblete)
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
	meses_trabajados_despues_del_ano = fields.Float(
		string='Meses Fraccionados',)
	dias_trabajados_luego_de_liquidacion = fields.Float(
		string='Dias Trabajados',)
	)