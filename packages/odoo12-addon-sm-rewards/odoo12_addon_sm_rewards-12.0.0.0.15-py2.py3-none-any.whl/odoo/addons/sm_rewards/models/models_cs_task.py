# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _


class cs_task(models.Model):
    _name = 'project.task'
    _inherit = 'project.task'

    related_reward_id = fields.Many2one(
        'sm_rewards.sm_reward', string=_("Reward"))
