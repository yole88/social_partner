# -- coding: utf-8 --

import datetime

from odoo import fields
from odoo.exceptions import ValidationError
import base64
import os
from odoo.tests.common import TransactionCase
from odoo.modules.module import get_module_resource

class TestResPartner(TransactionCase):

    def setUp(self):
        super(TestResPartner, self).setUp()
        # Set up the test images
        self.incomplete_image_path = get_module_resource('social_partner', 'static/src/img/incomplete.png')
        self.complete_image_path = get_module_resource('social_partner', 'static/src/img/complete.png')
        with open(self.incomplete_image_path, 'rb') as f:
            self.incomplete_image = base64.b64encode(f.read())
        with open(self.complete_image_path, 'rb') as f:
            self.complete_image = base64.b64encode(f.read())
    
    def test_complete_profile_computation(self):
        # Create a partner without social media links
        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'social_twitter': '',
            'social_facebook': '',
            'social_linkedin': ''
        })
        self.assertFalse(partner.complete_profile, "Profile should be incomplete without social media links.")
        self.assertEqual(partner.image_1920, self.incomplete_image)
        self.assertEqual(partner.image_128, self.incomplete_image)

        # Add social media links and check if profile is complete
        partner.write({
            'social_twitter': 'https://twitter.com/test',
            'social_facebook': 'https://facebook.com/test',
            'social_linkedin': 'https://linkedin.com/in/test'
        })
        self.assertTrue(partner.complete_profile, "Profile should be complete with all social media links.")
        self.assertEqual(partner.image_1920, self.complete_image)
        self.assertEqual(partner.image_128, self.complete_image)

if _name_ == '_main_':
    unittest.main()
