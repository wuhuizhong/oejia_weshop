# coding=utf-8

from openerp import models, fields, api


class res_partner(models.Model):

    _inherit = 'res.partner'

    province_id = fields.Many2one('oe.province', string='省')
    city_id = fields.Many2one('oe.city', string='市')
    district_id = fields.Many2one('oe.district', string='区')
    # street 详细地址
    is_default = fields.Boolean('是否为默认地址')
    city_domain_ids = fields.One2many('oe.city', compute='_compute_city_domain_ids')
    district_domain_ids = fields.One2many('oe.district', compute='_compute_district_domain_ids')
    
    """
    唯一性验证
    方法一：利用_sql_contraints
    注意：如果添加_sql_contraints前已经存在相同数据的字段，则_sql_contraints是添加不上的，因此也不会有提示出现。
    """
    _sql_constraints = [(
        'res_partner_name_unique',
        'UNIQUE (name)',
        '名字已存在！'
    )]

    """
    方法二：
    @api.contrains('name')
    def _check_name(self):
        partners = self.search([('name', '=', self.name)])
        if len(partners) > 1:
            raise ValueError('名字%s已存在!'%self.name)
    """

    @api.onchange('province_id')
    def _onchange_province_id(self):
        self.city_domain_ids = self.province_id.child_ids if self.province_id else False
        self.city_id = False
        self.district_id = False
        return {
            'domain': {
                'city_id': [('id', 'in', self.city_domain_ids.ids if self.city_domain_ids else [0])]
            }
        }

    @api.onchange('city_id')
    def _onchange_city_id(self):
        self.district_domain_ids = self.city_id.child_ids if self.city_id else False
        self.district_id = False
        return {
            'domain': {
                'district_id': [('id', 'in', self.district_domain_ids.ids if self.district_domain_ids else [0])]
            }
        }

    @api.depends('province_id')
    def _compute_city_domain_ids(self):
        self.city_domain_ids = self.province_id.child_ids if self.province_id else False

    @api.depends('city_id')
    def _compute_district_domain_ids(self):
        self.district_domain_ids = self.city_id.child_ids if self.city_id else False
