from odoo import _, models, fields, api
from odoo.exceptions import ValidationError, UserError


class SubscriptionRequest(models.Model):
    _inherit = 'subscription.request'
    _name = "subscription.request"

    related_reward_id = fields.Many2one(
        'sm_rewards.sm_reward', string=_("Related Reward"))
