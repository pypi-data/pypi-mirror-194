# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from html.parser import HTMLParser
from odoo import models, fields, api
from odoo.tools.translate import _


class sm_reward(models.Model):
    _name = 'sm_rewards.sm_reward'
    _inherit = 'sm_rewards.sm_reward'
    _description = "CS Reward"

    data_partner_creation_type = fields.Selection([
        ("none", "Nothing to do"),
        ("new", "Create new partner"),
        ("existing", "Find existing partner"),
        ("subscription", "Create new subscription request")],
        string=_("Partner creation type"),
        default="none",
        required=True
    )
    related_subscription_ids = fields.One2many(
        'subscription.request', 'related_reward_id', string=_("Related Subscriptions"))

    def compute_member(self):
        validation = super()._validate_membership()
        if validation['valid']:
            super().compute_member()
            if self.data_partner_creation_type == 'subscription':
                self.create_subscription()
            self.set_status('member')
            return {
                'valid': True
            }
        else:
            return {
                'valid': False,
                'error': validation['error']
            }

    def create_subscription(self):
        product = self.env['product.product'].search(
            [('name', '=', 'Quota de soci')])
        subscription_creation_data = {
            'name': self.data_partner_firstname + ' ' + self.data_partner_lastname,
            'firstname': self.data_partner_firstname,
            'lastname': self.data_partner_lastname,
            'vat': self.data_partner_vat,
            'email': self.data_partner_email,
            'mobile': self.data_partner_mobile,
            'phone': self.data_partner_phone,
            'gender': self.data_partner_gender,
            'birthdate': self.data_partner_birthdate_date,
            'address': self.data_partner_street,
            'zip_code': self.data_partner_zip,
            'state_id': self.data_partner_state_id.id,
            'country_id': self.data_partner_state_id.country_id.id,
            'city': self.data_partner_city,
            'driving_license_expiration_date': self.data_partner_driving_license_expiration_date,
            'image_dni': self.data_partner_image_dni,
            'image_driving_license': self.data_partner_image_driving_license,
            'iban': self.data_partner_iban,
            'date': datetime.now(),
            'source': 'crm',
            'ordered_parts': 1,
            'share_product_id': product.id,
            'lang': 'ca_ES',
            'related_reward_id': self.id
        }
        subscription = self.env['subscription.request'].create(
            subscription_creation_data)
        subscription.validate_subscription_request()
        self.related_member_id = subscription.partner_id
