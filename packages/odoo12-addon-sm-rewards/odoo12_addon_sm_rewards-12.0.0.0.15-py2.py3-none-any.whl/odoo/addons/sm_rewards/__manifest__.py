# -*- coding: utf-8 -*-
{
    'name': "sm_rewards",

    'summary': """""",

    'description': """""",

    'author': "Som Mobilitat",
    'website': "http://www.sommobilitat.coop",

    'category': 'vertical-carsharing',
    'version': '12.0.0.0.15',

    # any module necessary for this one to work correctly
    # 'sm_partago_db','sm_partago_invoicing','sm_carsharing_structure'
    'depends': [
        'base',
        'mail',
        'account',
        'vertical_carsharing',
        'sm_partago_user',
        'fleet', 'sm_pocketbook',
        'sm_partago_tariffs',
        'sm_partago_usage'
    ],

    # always loaded
    'data': [
        'email_tmpl/cs_reward_completed_email.xml',
        'email_tmpl/cs_reward_soci_not_found_email.xml',
        'security/ir.model.access.csv',
        'views/views_res_config_settings.xml',
        'views/views_cs_car_service.xml',
        'views/views_pocketbook_record.xml',
        'views/views_cs_registration_request.xml',
        'views/views_reward.xml',
        'views/views_members.xml',
        'views/views_reward_actions.xml',
        'views/views_cron.xml',
        'views/views_tariff.xml',
        'views/views_reservation_compute.xml',
        'views/views_cs_task.xml'
    ],
    # only loaded in demonstration mode
    'demo': [],
}
