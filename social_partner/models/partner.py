# -*- coding: utf-8 -*-

from odoo import api, models, fields, modules
import base64


class ResPartner(models.Model):
    _inherit = 'res.partner'


    social_twitter = fields.Char('Twitter')
    social_facebook = fields.Char('Facebook')
    social_linkedin = fields.Char('Linkedin')
    complete_profile = fields.Boolean(compute='_compute_complete_profile', store=True, string='Complete Profile')

    @api.depends('social_twitter', 'social_facebook', 'social_linkedin')
    def _compute_complete_profile(self):
        for partner in self:
            complete_profile = False
            path_img = 'static/src/img/incomplete.png'
            image_path = modules.get_module_resource('social_partner', path_img)
            self.image_1920 = base64.b64encode(open(image_path, 'rb').read())
            self.image_128 = base64.b64encode(open(image_path, 'rb').read())

            if partner.social_twitter and partner.social_facebook and partner.social_linkedin:
                complete_profile = True
                path_img = 'static/src/img/complete.png'
                image_path = modules.get_module_resource('social_partner', path_img)
                self.image_1920 = base64.b64encode(open(image_path, 'rb').read())
                self.image_128 = base64.b64encode(open(image_path, 'rb').read())

            partner.complete_profile = complete_profile
