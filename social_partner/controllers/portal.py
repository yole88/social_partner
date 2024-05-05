# -*- coding: utf-8 -*-
import binascii

from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from collections import OrderedDict
from odoo.osv.expression import AND, OR


class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        Partners = request.env['res.partner']
        if 'partner_count' in counters:
            values['partner_count'] = Partners.search_count([]) \
                if Partners.check_access_rights('read', raise_exception=False) else 0
        return values

    def _get_partner_searchbar_sortings(self):
        return {
            'date': {'label': _('Create date'), 'order': 'create_date desc'},
            'name': {'label': _('Reference'), 'order': 'name'},
        }

    def _get_searchbar_inputs(self):
        return {
            'content': {'input': 'content', 'label': _('Search <span class="nolabel"> (in Content)</span>')},
            'name': {'input': 'name', 'label': _('Search in Name')},
            'social_facebook': {'input': 'social_facebook', 'label': _('Search in Facebook')},
            'social_linkedin': {'input': 'social_linkedin', 'label': _('Search in Linkedin')},
            'social_twitter': {'input': 'social_twitter', 'label': _('Search in Twitter')}
        }

    def _get_search_domain(self, search_in, search):
        search_domain = []
        if search_in in ('content', 'all'):
            search_domain = OR([search_domain, ['|', '|', '|',('name', 'ilike', search), ('social_facebook', 'ilike', search), ('social_linkedin', 'ilike', search), ('social_twitter', 'ilike', search)]])
        if search_in in ('name', 'all'):
            search_domain = OR([search_domain, [('name', 'ilike', search)]])
        if search_in in ('social_facebook', 'all'):
            search_domain = OR([search_domain, [('social_facebook', 'ilike', search)]])
        if search_in in ('social_linkedin', 'all'):
            search_domain = OR([search_domain, [('social_linkedin', 'ilike', search)]])
        if search_in in ('social_twitter', 'all'):
            search_domain = OR([search_domain, [('social_twitter', 'ilike', search)]])
        return search_domain

    @http.route(['/my/partners', '/my/partners/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_partners(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None, search_in='all', **kw):
        values = self._prepare_portal_layout_values()
        Partners = request.env["res.partner"]

        domain = []

        searchbar_sortings = self._get_partner_searchbar_sortings()

        searchbar_inputs = self._get_searchbar_inputs()

        # default sortby order
        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'complete_profile': {'label': _('Profile complete'), 'domain': [('complete_profile', '=', True)]},
            'incomplete_profile': {'label': _('Profile incomplete'), 'domain': [('complete_profile', '=', False)]},
        }
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        if search and search_in:
            domain += self._get_search_domain(search_in, search)

        # count for pager
        partner_count = Partners.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/partners",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'search_in': search_in, 'search': search},
            total=partner_count,
            page=page,
            step=self._items_per_page
        )

        # search the count to display, according to the pager data
        partners = Partners.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_partners_history'] = partners.ids[:100]

        values.update({
            'date': date_begin,
            'partners': partners.sudo(),
            'page_name': 'partner',
            'pager': pager,
            'default_url': '/my/partners',
            'searchbar_sortings': searchbar_sortings,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return request.render("social_partner.portal_my_partners", values)
