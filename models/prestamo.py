# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import date, datetime, time
import logging

_logger = logging.getLogger(__name__)

class prestamo_prestciones(models.Model):
    _name='prestamo'
    # Barra de Empleados
    name = fields.Many2one('hr.employee',
    string='Empleado',
    required=True)
    monto_prestamo = fields.Float(
    string='Monto del Prestamo',
    store=True,
    required=True,
    digits=(16,2))
    fecha_actual = fields.Date(
    string='Fecha Actual',
    required= True,
    default=lambda self: fields.Date.to_string(date.today()),
    readonly=True)
    metodo_pago = fields.Selection(
    string='Metodo de Pago',
    selection=[('nomina','Nómina'),
                # ('externo','Externo')
                ],
    required=True)
    cuotas= fields.Float(
    string= 'N° de Cuotas',
    store=True,
    digits=(16,2),
    default=1.0)
    fecha_cobro = fields.Date(
    string='Fecha Incial',
    required=True)

    @api.multi
    @api.depends('name')
    def _MontoMaximoDisponible(self):
        for record in self:
            if record.name.id != False:
                self._cr.execute('SELECT acumulado_al_ano FROM prest WHERE name = '+str(record.name.id)+ 'ORDER BY id DESC LIMIT 1')
                variable = self._cr.fetchall()
                record.monto_maximo = float((variable[0])[0])
    monto_maximo = fields.Float(
    string='Monto Máximo Disponible',
    compute = '_MontoMaximoDisponible',
    store=True,
    default=1.0)
    monto = fields.Float(
    string='Monto a Cancelar',
    store=True,
    digits=(16,2))
    cuotas_cancelada= fields.Float(
    string= 'Cuota a Cancelar',
    store=True,
    digits=(16,2),
    default=1.0)
    fecha_cancelada = fields.Date(
    string='Fecha del Pago',
    required=True)

    @api.depends('name')
    def _MontoCancelado(self):
        for record in self:
            
            record.monto_cancelado == monto
    monto_cancelado = fields.Float(
        string= 'Monto Cancelado'
    )