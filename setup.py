__menu = {
    'uri': __package__,
    'name': '편집기',
    'list': [
        {
            'uri': '',
            'name': '편집기',
        },
        {
            'uri': 'setting',
            'name': '설정',
        },
        {
            'uri': 'manual',
            'name': '매뉴얼',
            'list': [
                {
                    'uri': 'README.md',
                    'name': 'README'
                }
            ]
        },
    ]
}

setting = {
    'filepath' : __file__,
    'use_db': True,
    'use_default_setting': True,
    'home_module': 'setting',
    'menu': __menu,
    'setting_menu': {
        'uri': f"{__package__}/setting",
        'name': '편집기 설정',
    },
    'default_route': None,
}

from plugin import *
P = create_plugin_instance(setting)

from framework import F, login_required
from .mod_setting import ModuleSetting
P.set_module_list([ModuleSetting])



@P.blueprint.route('/setting', methods=['GET', 'POST'])
@login_required
def second_menu():
    from flask import request
    return P.module_list[0].process_menu('', request)

@P.blueprint.route('/ajax/<sub>', methods=['GET', 'POST'])
@login_required
def ajax(sub):
    if sub == 'setting_save':
        ret = P.ModelSetting.setting_save(request)
        for module in P.module_list:
            module.setting_save_after()
        return jsonify(ret)