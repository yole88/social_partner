# -- coding: utf-8 --
from odoo.tests.common import HttpCase, tagged

@tagged('-at_install', 'post_install')
class TestCustomerPortal(HttpCase):

    def setUp(self):
        super(TestCustomerPortal, self).setUp()
        self.env = self.env(user=SUPERUSER_ID)
        self.partner1 = self.env['res.partner'].create({
            'name': 'Test Partner 1',
            'social_twitter': 'https://twitter.com/test1',
            'social_facebook': 'https://facebook.com/test1',
            'social_linkedin': 'https://linkedin.com/in/test1',
            'complete_profile': True
        })
        self.partner2 = self.env['res.partner'].create({
            'name': 'Test Partner 2',
            'social_twitter': '',
            'social_facebook': '',
            'social_linkedin': '',
            'complete_profile': False
        })

    def test_portal_my_partners(self):
        # Log in as demo user
        self.authenticate('demo', 'demo')

        # Access the partner list
        response = self.url_open('/my/partners')
        self.assertEqual(response.status_code, 200, "Failed to load /my/partners page")

        # Test search functionality
        response = self.url_open('/my/partners?search=test1&search_in=name')
        self.assertEqual(response.status_code, 200, "Failed to search partners by name")
        self.assertIn('Test Partner 1', response.text, "Partner not found in search results")

        # Test filter functionality
        response = self.url_open('/my/partners?filterby=complete_profile')
        self.assertEqual(response.status_code, 200, "Failed to filter partners by complete profile")
        self.assertIn('Test Partner 1', response.text, "Complete profile partner not found in filtered results")
        self.assertNotIn('Test Partner 2', response.text, "Incomplete profile partner found in filtered results")

        # Test sort functionality
        response = self.url_open('/my/partners?sortby=name')
        self.assertEqual(response.status_code, 200, "Failed to sort partners by name")
        self.assertIn('Test Partner 1', response.text, "Partner not found in sorted results")

if _name_ == '_main_':
    unittest.main()
