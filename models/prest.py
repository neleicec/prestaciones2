# -*- coding: utf-8 -*- 

from odoo import models, fields, api
# CAMPOS TRIMESTRALES
class prest(models.Model):
	_name='prest'
	name = fields.Many2one('hr.employee', 
		string='Empleado', 
		required=True)
	trimestre = fields.Selection(
		string = 'Seleccione Trimestre', 
		selection=[('trimestre1', 'First Trimester'),('trimestre2','Second Trimester'),('trimestre3','Third Quarter'),('trimestre4','Fourth Trimester')],
		required=True,
		default='trimestre1', 
		help='Indique el trimestre a calcular')
	sueldo = fields.Float(
		string='Sueldo',
		digits=(16,2), 
		required=True, 
		related='name.wage1',
		readonly=True, 
		help="Basic Salary of the employee")
	vac_concepto= fields.Float(
		string='Concepto Vacaciones', 
		required=True, 
		related='name.concepto_vac', 
		readonly=True)
	tasa_trimestral=fields.Float(
		string='Tasa Trimestral',
		required=True)
	historicoPrestaciones = fields.Float(
		string='Histórico', 
		required=True, 
		related='name.historico_prestaciones', 
		readonly=True)

 	def _dias(self):
		return 15
	dias_metodo_trimestral = fields.Integer(
		string='Dias', 
		default=_dias, 
		readonly=True,
		store=True)

	@api.depends('name')
	def _saldia(self):
		for record in self:
			record.salario_diario = record.sueldo / 30
	salario_diario= fields.Float(
		string='Salario Diario', 
		digits=(26,2), 
		compute='_saldia', 
		readonly=True,
		store=True)

	@api.depends('name')
	def _alic(self):
		for record in self:
			record.alicuota_utilidades = (((record.sueldo/30) * 30)/360)
	alicuota_utilidades= fields.Float(
		string='Alicuota Utilidades', 
		digits=(26,2),
		compute='_alic', 
		readonly=True,
		store=True)

	@api.depends('name')
	def _vac(self):
		for record in self:
			record.alicuota_vacaciones = ((record.sueldo/30)*(record.vac_concepto) / 360)
	alicuota_vacaciones= fields.Float(
		string='Alicuota Vacaciones', 
		digits=(26,2), 
		compute='_vac',
		store=True)

	@api.depends('name')
	def _int(self):
		for record in self:
			record.salario_integral = ((record.sueldo/30)+ record.alicuota_utilidades + record.vac_concepto)
	salario_integral= fields.Float(
		string='Salario Integral', 
		digits=(26,2), 
		readonly=True,
		compute='_int',
		store=True)

	@api.depends('name')
	def _total1(self):
		for record in self:
			record.prestamo_trimestral = (record.salario_integral * record.dias_metodo_trimestral)
	prestamo_trimestral= fields.Float(
		string='Trimestre', 
		readonly=True, 
		compute='_total1',
		store=True)

	@api.depends('trimestre')
	def _trim(self):
		for record in self:
			if record.trimestre == 'trimestre4':
				record.prestamo_adicional = (record.salario_integral * record.dias_adicionales) 
				record.acumulado_al_ano = (record.prestamo_trimestral + record.prestamo_adicional)
	prestamo_adicional= fields.Float(
		string='Acumulado Adicional', 
		readonly=True, 
		compute='_trim',
		store=True,
		help='Indica cuánto lleva acumulado el empleado por los dias adicionales')			
	acumulado_al_ano= fields.Float(
		string='Acumulado al año',
		readonly=True,
		compute='_trim',
		required=True,
		default= 0.0,
		digits=(26,2),
		store=True,
		help= 'indica el monto acumulado durante los "4" trimestres del año')

	# CAMPOS ANUALES 

	@api.depends('name')
	def _diah(self):
		for record in self:
			if (record.name.years_service) <= 2.0:
				dias_adicionales = 0.0
			else: 
				years_service2 = float(record.name.years_service)
				sumador = years_service2 - 1.0
				sumadorx = sumador * 2.0 
				record.dias_adicionales = sumadorx
				if(record.dias_adicionales) >=30.0:
					record.dias_adicionales=30
	dias_adicionales= fields.Float(
		string='Dias Adicionales', 
		digits=(26,2), 
		readonly=True, 
		compute='_diah',
		store=True)
	@api.depends('tasa_trimestral')
	def _tasat(self):
		for record in self:
			record.interes_trimestral = (record.tasa_trimestral * record.prestamo_trimestral) / 1200
	interes_trimestral=fields.Float(
		string='Interes Trimestral',
		compute='_tasat',
		store=True)




# Crar campo Wage1 en Empleado

class employee(models.Model):
	_inherit='hr.employee'
	wage1 = fields.Float('Wage', 
		digits=(16,2), 
		required=True,
		store=True)
	concepto_vac = fields.Float(
		string='Concepto Vacaciones', 
		required=True, 
		help="Número de días que le pagan al trabajador por concepto de vacaciones",
		store=True)
	historico_prestaciones = fields.Float(
		string = 'Historico Prestaciones',
		digits = (16,2),
		store = True)