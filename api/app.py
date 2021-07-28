import os
import subprocess
import time
import zipfile
import shutil
from pathlib import Path

from flask import Flask, Request, Response
from flask import render_template
from flask import flash, request, redirect, url_for
from flask import send_from_directory
from flask_session import Session
from werkzeug.utils import secure_filename

# export PYTHONPATH=$PYTHONPATH:/media/data-huy/3D_Reconstruction/Github/openMVG/data
# os.environ['PYTHONPATH'] = '/media/data-huy/3D_Reconstruction/Github/openMVG/data'
from extract_frames import extract_frames_from_video


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))


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

app = Flask(__name__)
sess = Session()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1000 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and \
	    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        global PROCESS_COMPLETE
        PROCESS_COMPLETE = False
        os.chdir(MAIN_WORKING_DIR)
        # check if the post request has the file part
        if 'file' not in request.files:
           flash('No file part')
           return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
           flash('No selected file')
           return redirect(request.url)
        if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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
           global approx_focal
           approx_focal = extract_frames_from_video(filename=filename, 
                                                    type_of_extraction=type_of_extraction, 
                                                    extraction_number=int(extraction_number), 
                                                    interleaved_number=int(interleaved_number))
           time.sleep(3)
           cwd = os.getcwd()
           os.chdir('../openMVG')
           if Path('./output_images').is_dir():
              shutil.rmtree('./output_images')
           if Path('./Output.zip').is_file():
              os.remove('./Output.zip')
           #reconstruct_3d_model(approx_focal, feature_quality, resolution_scale)
           return redirect(url_for('process_3d'))
           # return redirect(url_for('download_file', name='Output.zip'))
    
    return render_template('upload.html')


def my_exec(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    # print(popen.stdout)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

@app.route('/process', methods=['GET', 'POST'])
def process_3d():
    # if request.headers.get('accept') == 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8':
    if PROCESS_COMPLETE == False and request.headers.get('accept') == 'text/event-stream':
        def reconstruct_3d_model(focal, quality, scale):
            error_flag = False
            # for i, c in enumerate(itertools.cycle('\|/-')):
            #     yield "data: %s %d\n\n" % (c, i)
            #     time.sleep(.1)  # an artificial delay
            start_time = time.time()
            os.chdir('./openMVG_Build/software/SfM')
            try:
                for path in my_exec(['python', 'SfM_GlobalPipeline.py', '/media/data-huy/3D_Reconstruction/openMVG/data/images', 
                                                                    '/media/data-huy/3D_Reconstruction/openMVG/output_images',
                                                                    str(focal),
                                                                    str(quality)]):
                    yield "data: [In progress] %s\n\n" % (path)
            except:
                error_flag = True
                yield "data: [Error] Need to try with another parameter set (e.g.: higher feature quality, higher interleaved number, ...)\n\n"

            # subprocess.run(['cd', '../..'])
            os.chdir('../..')
            # subprocess.run(['cd', 'Linux-x86_64-RELEASE/'])
            os.chdir('Linux-x86_64-RELEASE/')
            if not error_flag:
                try:
                    for path in my_exec(['mkdir', '/media/data-huy/3D_Reconstruction/openMVG/output_images/stereo_vision']):
                        yield "data: [In progress] %s\n\n" % (path)
                except:
                    error_flag = True
                    yield "data: [Error] Need to try with another parameter set (e.g.: higher feature quality, higher interleaved number, ...)\n\n"

            if not error_flag:
                try:
                    for path in my_exec(['./openMVG_main_openMVG2openMVS', '-i', '/media/data-huy/3D_Reconstruction/Github/openMVG/output_images/reconstruction_global/robust.bin', 
                                                                    '-d', '/media/data-huy/3D_Reconstruction/Github/openMVG/output_images/stereo_vision', 
                                                                    '-o', '/media/data-huy/3D_Reconstruction/Github/openMVG/output_images/stereo_vision/Scene.mvs']):
                        yield "data: [In progress] %s\n\n" % (path)
                except:
                    error_flag = True
                    yield "data: [Error] Need to try with another parameter set (e.g.: higher feature quality, higher interleaved number, ...)\n\n"
            # subprocess.run(['export', 'PATH="/media/data-huy/bin/OpenMVS:$PATH']) 
            os.environ["PATH"] += os.pathsep + "/media/data-huy/bin/OpenMVS"
            # subprocess.run(['cd', '../../output_images/stereo_vision/'])
            os.chdir('../../output_images/stereo_vision/')
            if not error_flag:
                try:
                    for path in my_exec(['DensifyPointCloud', 'Scene.mvs']):
                        yield "data: [In progress] %s\n\n" % (path)
                except:
                    error_flag = True
                    yield "data: [Error] Need to try with another parameter set (e.g.: higher feature quality, higher interleaved number, ...)\n\n"
            if not error_flag:
                try:
                    for path in my_exec(['ReconstructMesh', 'Scene_dense.mvs']):
                        yield "data: [In progress] %s\n\n" % (path)
                except:
                    error_flag = True
                    yield "data: [Error] Need to try with another parameter set (e.g.: higher feature quality, higher interleaved number, ...)\n\n"
            if not error_flag:
                try:
                    for path in my_exec(['TextureMesh', 'Scene_dense_mesh.mvs', ''.join(['--resolution-level=', str(scale)])]):
                        yield "data: [In progress] %s\n\n" % (path)
                except:
                    error_flag = True
                    yield "data: [Error] Need to try with another parameter set (e.g.: higher feature quality, higher interleaved number, ...)\n\n"
            os.chdir('../..')

            end_time = time.time()
            hours, rem = divmod(end_time - start_time, 3600)
            minutes, seconds = divmod(rem, 60)
            # print("[+] Execution time: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
            time.sleep(3)
            if not error_flag:
                zipf = zipfile.ZipFile('Output.zip', 'w', zipfile.ZIP_DEFLATED)
                zipdir('output_images/', zipf)
                zipf.close()
                yield "data: [Complete] Execution time: %s:%s:%s \n\n" % (int(hours), int(minutes), int(seconds))
            global PROCESS_COMPLETE
            PROCESS_COMPLETE = True
        return Response(reconstruct_3d_model(approx_focal, feature_quality, resolution_scale), content_type='text/event-stream')
    return redirect(url_for('static', filename='command.html'))

       

@app.route('/<name>', methods=['GET', 'POST'])
def download_file(name):
    # cwd = os.getcwd()
    # os.chdir('../openMVG')
    DOWNLOAD_FOLDER = os.getcwd()
    print('[+] DOWNLOAD_FOLDER: ', DOWNLOAD_FOLDER)
    app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
    down_file = send_from_directory(app.config["DOWNLOAD_FOLDER"], name, as_attachment=True)
    # os.chdir('../api')
    # os.chdir(cwd)	
    return down_file

app.add_url_rule(
    "/<name>", endpoint="download_file", build_only=True
)


if __name__ == "__main__":
   app.secret_key = 'super secret key'
   app.config['SESSION_TYPE'] = 'filesystem'

   sess.init_app(app)

   app.debug = True
   app.run()