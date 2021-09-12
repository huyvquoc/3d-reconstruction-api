import os

from flask import current_app, Blueprint
from flask import Flask, Request, Response
from flask import render_template
from flask import flash, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename

from .tasks import make_file, reconstruct_3d_model


bp = Blueprint("all", __name__)

cwd = os.getcwd()
print("[+] In app.py, print os.getcwd(): ", cwd)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'mp4'}
PROCESS_COMPLETE = False
MAIN_WORKING_DIR = os.getcwd() # Path to the 'api' folder
type_of_extraction = None
extraction_number = None
interleaved_number = None
feature_quality = None
resolution_scale = None
approx_focal = None

@bp.route("/")
def index():
    return "Hello!"

@bp.route("/<string:fname>/<string:content>")
def makefile(fname, content):
    fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    make_file(fpath, content)
    return f"Find your file @ <code>{fpath}</code>"

def allowed_file(filename):
    return '.' in filename and \
	    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route("/3d_reconstruction", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print('1')
        global PROCESS_COMPLETE
        PROCESS_COMPLETE = False
        os.chdir(MAIN_WORKING_DIR)
        # check if the post request has the file part
        print('2')
        if 'file' not in request.files:
           flash('No file part')
           return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        print('3')
        if file.filename == '':
           flash('No selected file')
           return redirect(request.url)
        print('4')
        if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)
           file.save(os.path.join(UPLOAD_FOLDER, filename))
           #return redirect(url_for('download_file', name=filename))
           global type_of_extraction
           global extraction_number
           global interleaved_number
           global feature_quality
           global resolution_scale
           type_of_extraction = request.form['frame_extraction']
           extraction_number = request.form['num_frames']
           interleaved_number = request.form['interleave']
           feature_quality = request.form['feat']
           resolution_scale = request.form['res']
           print('[+] type of extraction: ', type_of_extraction)
           print('[+] extraction_number: ', extraction_number)
           print('[+] interleaving frame: ', interleaved_number)
           print('[+] feature quality: ', feature_quality)
           print('[+] resolution scale: ', resolution_scale)
           # global approx_focal
           # cwd = os.getcwd()
           # os.chdir('../openMVG')
           # if Path('./output_images').is_dir():
              # shutil.rmtree('./output_images')
           # if Path('./Output.zip').is_file():
              # os.remove('./Output.zip')
           # down_file = reconstruct_3d_model.delay(filename, type_of_extraction, extraction_number, interleaved_number, 
           #                          feature_quality, resolution_scale)
           res = reconstruct_3d_model.delay(filename, type_of_extraction, extraction_number, interleaved_number,
                                    feature_quality, resolution_scale)

           # return redirect(url_for('process_3d'))
           # DOWNLOAD_FOLDER = os.getcwd()
           # print('[+] DOWNLOAD_FOLDER: ', DOWNLOAD_FOLDER)
           # app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
           # down_file = send_from_directory(app.config["DOWNLOAD_FOLDER"], 'Output.zip', as_attachment=True)
           # os.chdir(MAIN_WORKING_DIR)

           # return down_file
    return render_template('upload.html')