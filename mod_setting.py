from .setup import *
from flask import g

name = 'setting'

class ModuleSetting(PluginModuleBase):
    db_default = {
        f"{name}_root" : F.config['path_data'],
        f"{name}_exclude_foldernames" : 'mnt, __pycache__, .git, false',
        f"{name}_excluded_extensions" : 'mp4, db, pyo',
    }

    def __init__(self, P):
        super(ModuleSetting, self).__init__(P, name=name)


    def process_menu(self, page, req):
        arg = P.ModelSetting.to_dict()
        arg['module'] = self.name
        arg['page'] = page
        arg['path_app'] = F.config['path_app']
        arg['path_data'] = F.config['path_data']
        try:
            return render_template(f'{__package__}_{name}.html', arg=arg)
        except Exception as e: 
            P.logger.error(f'Exception:{str(e)}')
            P.logger.error(traceback.format_exc())
            return render_template('sample.html', title=f"{__package__}/{name}/{page}")


    def setting_save_after(self):
        g.flaskcode_resource_basepath = P.ModelSetting.get(f"{name}_root")


    def plugin_load(self):
        P.ModelSetting.set(f"{name}_root", F.config['path_data'])
