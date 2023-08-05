# -*- coding: utf-8 -*-
{
    'name': "sm_rewards_emc",

    'summary': """""",

    'description': """""",

    'author': "Som Mobilitat",
    'website': "http://www.sommobilitat.coop",

    'category': 'Uncategorized',
    'version': '12.0.0.0.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sm_rewards', 'easy_my_coop'],

    # always loaded
    'data': [
        'views/views_reward.xml',
        'views/views_subscription_request.xml'
    ],
    # only loaded in demonstration mode
    'demo': [],
}
