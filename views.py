# -*- coding: utf-8 -*-
import mimetypes
import os

from flask import (abort, g, jsonify, redirect, render_template, request,
                   send_file)
from framework import F, login_required

from .setup import P
from .utils import dir_tree, get_file_extension, write_file


def get_exclude_extensions():
    return P.ModelSetting.get_list('setting_excluded_extensions', ',')

def get_exclude_names():
    from .setup import P
    return P.ModelSetting.get_list('setting_exclude_foldernames', ',')


@P.blueprint.route('/') 
@login_required
def index():
    openfile = request.args.get('open')
    if openfile != None:
        if openfile.startswith(F.config['path_data']):
            openpath = openfile.replace(F.config['path_data'], '')
            g.flaskcode_resource_basepath = F.config['path_data']
        elif openfile.startswith(F.config['path_app']):
            openpath = openfile.replace(F.config['path_app'], '')
            P.ModelSetting.set('setting_root', F.config['path_app'])
        else:
            os.path.split(openfile)
            openpath = openfile.replace(F.config['path_data'], '')
            g.flaskcode_resource_basepath = F.config['path_data']
        if openpath.startswith('/') or openpath.startswith('\\'):
            tmp = openpath.replace('\\', '/')
            return redirect(f"/flaskcode{tmp}")
        else:
            return redirect(f'/flaskcode/{openpath}')
    dirname = os.path.basename(g.flaskcode_resource_basepath)
    dtree = dir_tree(g.flaskcode_resource_basepath, g.flaskcode_resource_basepath + '/', exclude_names=get_exclude_names(), excluded_extensions=get_exclude_extensions(), )
    return render_template('flaskcode/index.html', dirname=dirname, dtree=dtree, file_loading="")


@P.blueprint.route('/<path:path>')
@login_required
def index2(path):
    
    dirname = os.path.basename(g.flaskcode_resource_basepath)
    dtree = dir_tree(g.flaskcode_resource_basepath, g.flaskcode_resource_basepath + '/', exclude_names=get_exclude_names(), excluded_extensions=get_exclude_extensions(), )
    file_path = os.path.join(g.flaskcode_resource_basepath, path)
    if os.path.isfile(file_path):
        file_loading = path
    else:
        file_loading = ''
    return render_template('flaskcode/index.html', dirname=dirname, dtree=dtree, file_loading=file_loading)

@P.blueprint.route('/resource-data/<path:file_path>.txt', methods=['GET', 'HEAD'])
@login_required
def resource_data(file_path):
    file_path = os.path.join(g.flaskcode_resource_basepath, file_path)
    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        abort(404)
    response = send_file(file_path, mimetype='text/plain')
    mimetype, encoding = mimetypes.guess_type(file_path, False)
    if mimetype:
        response.headers.set('X-File-Mimetype', mimetype)
        extension = mimetypes.guess_extension(mimetype, False) or get_file_extension(file_path)
        if extension:
            response.headers.set('X-File-Extension', extension.lower().lstrip('.'))
    if encoding:
        response.headers.set('X-File-Encoding', encoding)
    return response


@P.blueprint.route('/update-resource-data/<path:file_path>', methods=['POST'])
@login_required
def update_resource_data(file_path):
    file_path = os.path.join(g.flaskcode_resource_basepath, file_path)
    is_new_resource = bool(int(request.form.get('is_new_resource', 0)))
    if not is_new_resource and not (os.path.exists(file_path) and os.path.isfile(file_path)):
        abort(404)
    success = True
    message = 'File saved successfully'
    resource_data = request.form.get('resource_data', None)
    if resource_data:
        success, message = write_file(resource_data, file_path)
    else:
        success = False
        message = 'File data not uploaded'
    return jsonify({'success': success, 'message': message})
