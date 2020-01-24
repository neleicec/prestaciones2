#  -*- coding: utf-8 -*- 

from odoo import models, fields, api, exceptions
from datetime import date, datetime, time
import logging

_logger = logging.getLogger(__name__)

class anticipo_prestaciones(models.Model):
	_name='anticipo'

	# @api.multi
    # def action_topay(self):
	# 	self.write({'state': 'topay'})


	# Barra de empleados
	name = fields.Many2one('hr.employee', 
		string='Empleado', 
		required=True)
	# Muestra la Fecha de Ingreso
	tipo = fields.Selection( 
		string='Tipo del Anticipo',
        selection=[('normal','Normal'),('excepcional','Excepcional')],
		required=True)
    #Fecha en la que se solicito la Anticipación
   	fecha_actual = fields.Date(string='Fecha Actual', required=True,
        default=lambda self: fields.Date.to_string(date.today()),
		readonly=True)
	metodo_de_pago = fields.Selection( 
        string='Metodo de Pago',
        selection=[('nomina','Nómina'),
					# ('externo','Externo')
					],
        required=True)
	
	
	@api.multi
	@api.depends('name','tipo')
	def _anos_acumulados(self):
		for record in self:
			if record.name.id != False:
				self._cr.execute('SELECT acumulado_al_ano FROM prest WHERE name = '+str(record.name.id)+' ORDER BY id DESC LIMIT 1')
				variable = self._cr.fetchall()
				record.acumulado = float((variable[0])[0])
			if record.monto_anticipo == 0.0:
				return
			else:
				porcentaje=(record.monto_anticipo * 100.0 / record.acumulado)
			if (record.tipo == ('normal'))and(porcentaje > 75):
				raise exceptions.UserError('El monto solicitado sobrepasa los 75%')
				return
			elif (record.tipo == ('excepcional'))and(porcentaje > 100):
				raise exceptions.UserError('El monto solicitado sobrepasa los 100%')
				return
			
	acumulado = fields.Float(
		string='Record Acumulado',
		compute='_anos_acumulados',
		store=True,
		default=1.0)
	monto_anticipo = fields.Float(
		string='Monto del Anticipo',
		store=True,
		digits=(16,2))

    # @api.multi
    # def button_paid(self):
    #     for record in self:
    #         record.write({'state' : 'paid'})

    # @api.multi
    # def button_cancel(self):
    #     for record in self:
    #         record.write({'state' : 'cancel'})

	state = fields.Selection([
        ('paid', 'Pagado'),
        ('topay', 'Por Pagar'),
        ('cancel', 'Cancelado'),
        ], default='topay', readonly=True)
