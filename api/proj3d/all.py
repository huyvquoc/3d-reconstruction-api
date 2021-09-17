import os

from flask import current_app, Blueprint
from flask import Flask, Request, Response
from flask import render_template
from flask import flash, request, redirect, url_for
from flask import send_from_directory
from flask import jsonify
from werkzeug.utils import secure_filename
from pathlib import Path

from .tasks import reconstruct_3d_model


bp = Blueprint("all", __name__)

cwd = os.getcwd()
print("[+] In app.py, print os.getcwd(): ", cwd)

UPLOAD_FOLDER = './uploads'
DOWNLOAD_FOLDER = None
ALLOWED_EXTENSIONS = {'mp4'}
PROCESS_COMPLETE = False
MAIN_WORKING_DIR = os.getcwd() # Path to the 'api' folder
type_of_extraction = None
extraction_number = None
interleaved_number = None
feature_quality = None
resolution_scale = None
approx_focal = None

def allowed_file(filename):
    return '.' in filename and \
	    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route("/", methods=['GET', 'POST'])
def reconstruct3dmodel():
    if request.method == 'GET':
        return render_template('upload.html')
    if 'file' not in request.files:
        flash('No file part')
        # return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        # return redirect(request.url)

    type_of_extraction = request.form['frame_extraction']
    extraction_number = request.form['num_frames']
    interleaved_number = request.form['interleave']
    feature_quality = request.form['feat']
    resolution_scale = request.form['res']
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        task = reconstruct_3d_model.apply_async((filename, type_of_extraction, extraction_number, interleaved_number,
                                                feature_quality, resolution_scale))

        return jsonify({"task_id": task.id}), 202, {'Location': url_for('all.taskstatus',
                                                    task_id=task.id)}

@bp.route("/status/<task_id>")
def taskstatus(task_id):
    task = reconstruct_3d_model.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'step': "START",
            'progress': 0,
            'total': 1
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'step': task.info.get('step', ''),
            'progress': task.info.get('progress', 0),
            'total': task.info.get('total', 1)
        }
        if 'output_file' in task.info:
            response['output_file'] = task.info['output_file']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'step': str(task.info),
            'progress': 1,
            'total': 1
        }
    return jsonify(response)

@bp.route("/downloads/<path:filename>")
def download_file(filename):
    path = Path(os.getcwd())
    print('[**] path: ', path)
    parent_path = path.parent.absolute()
    print('[**] parent_path: ', parent_path)
    DOWNLOAD_FOLDER = os.path.join(parent_path, 'openMVG')
    print('[**] DOWNLOAD_FOLDER: ', DOWNLOAD_FOLDER)
    resp = send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
    os.remove(os.path.join(DOWNLOAD_FOLDER, filename))
    return resp