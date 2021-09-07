import os
import subprocess
import time
import datetime
import zipfile

from .celery import app
from extract_frames import extract_frames_from_video

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

@app.task()
def reconstruct_3d_model(filename, type_of_extraction, extraction_number, interleaved_number, 
                        feature_quality, resolution_scale):
    approx_focal = extract_frames_from_video(filename=filename,
                                            type_of_extraction=type_of_extraction, 
                                            extraction_number=int(extraction_number), 
                                            interleaved_number=int(interleaved_number))
    print(os.getcwd())
    cwd = os.getcwd()
    os.chdir('../openMVG')
    start_time = time.time()
    # subprocess.run(['cd', '../openMVG'])
    # subprocess.run(['cd', './openMVG_Build/software/SfM'])
    print(os.getcwd())
    os.chdir('./openMVG_Build/software/SfM')
    openmvg_path = "/media/data-huy/3D_Reconstruction/Github/openMVG"
    out_folder_name = "".join(["output_", datetime.datetime.now().strftime("%Y%m%d-%H%M%S")])
    subprocess.run(['python', 'SfM_GlobalPipeline.py', os.path.join(openmvg_path, 'data', 'images'), 
                                                       os.path.join(openmvg_path, out_folder_name),
                                                       str(approx_focal),
                                                       str(feature_quality)])
    os.chdir('../..')
    os.chdir('Linux-x86_64-RELEASE/')
    subprocess.run(['mkdir', os.path.join(openmvg_path, out_folder_name, 'stereo_vision')])
    subprocess.run(['./openMVG_main_openMVG2openMVS', '-i', os.path.join(openmvg_path, out_folder_name, 'reconstruction_global', 'robust.bin'), 
                                                      '-d', os.path.join(openmvg_path, out_folder_name, 'stereo_vision'), 
                                                      '-o', os.path.join(openmvg_path, out_folder_name, 'stereo_vision', 'Scene.mvs')])

    os.environ["PATH"] += os.pathsep + "/media/data-huy/bin/OpenMVS"
    os.chdir(os.path.join('../..', out_folder_name, 'stereo_vision/'))
    subprocess.run(['DensifyPointCloud', 'Scene.mvs'])
    subprocess.run(['ReconstructMesh', 'Scene_dense.mvs'])
    subprocess.run(['TextureMesh', 'Scene_dense_mesh.mvs', ''.join(['--resolution-level=', str(resolution_scale)])])
    os.chdir('../..')

    end_time = time.time()
    hours, rem = divmod(end_time - start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print("[+] Execution time: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

    zipf = zipfile.ZipFile("".join([out_folder_name, '.zip']), 'w', zipfile.ZIP_DEFLATED)
    zipdir(out_folder_name, zipf)
    zipf.close()
    os.chdir(cwd)

    return "".join([out_folder_name, '.zip'])
    # DOWNLOAD_FOLDER = os.getcwd()
    # print('[+] DOWNLOAD_FOLDER: ', DOWNLOAD_FOLDER)
    # app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
    # down_file = send_from_directory(app.config["DOWNLOAD_FOLDER"], "".join([out_folder_name, '.zip']), as_attachment=True)
    # os.chdir(cwd)

    # return down_file