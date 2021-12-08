import os
import subprocess
import time
import datetime
import zipfile
import shutil

from proj3d import celery 
from extract_frames import extract_frames_from_video


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

@celery.task(bind=True)
def reconstruct_3d_model(self, filename, type_of_extraction, extraction_number, interleaved_number, 
                        feature_quality, resolution_scale):
    self.update_state(state='PROGRESS',
                      meta={'step': "START", 'progress': 0, 'total': 7})
    cur_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    images_folder_name = "".join(["images_", cur_time])
    out_folder_name = "".join(["output_", cur_time])
    self.update_state(state='PROGRESS',
                      meta={'step': "EXTRACT FRAMES", 'progress': 1, 'total': 7})
    approx_focal = extract_frames_from_video(filename=filename,
                                            images_folder=images_folder_name,
                                            type_of_extraction=type_of_extraction, 
                                            extraction_number=int(extraction_number), 
                                            interleaved_number=int(interleaved_number))
    print(os.getcwd())
    cwd = os.getcwd()
    os.chdir('../openMVG')
    start_time = time.time()
    # subprocess.run(['cd', '../openMVG'])
    # subprocess.run(['cd', './openMVG_Build/software/SfM'])
    self.update_state(state='PROGRESS',
                      meta={'step': "SFM GLOBAL PIPELINE", 'progress': 2, 'total': 7})
    print(os.getcwd())
    os.chdir('./openMVG_Build/software/SfM')
    openmvg_path = "/media/data-huy/3D_Reconstruction/Github/openMVG" # TODO: change to the absolute path of the openMVG folder on your system
    # openmvg_path = "/opt/3dmodel/3D-Reconstruction/openMVG" # TODO: change to the absolute path of the openMVG folder on your system
    out_folder_name = "".join(["output_", datetime.datetime.now().strftime("%Y%m%d-%H%M%S")])
    subprocess.run(['python', 'SfM_GlobalPipeline.py', os.path.join(openmvg_path, 'data', images_folder_name),
                                                       os.path.join(openmvg_path, out_folder_name),
                                                       str(approx_focal),
                                                       str(feature_quality)])
    self.update_state(state='PROGRESS',
                      meta={'step': "CONVERT OPENMVG TO OPENMVS", 'progress': 3, 'total': 7})
    os.chdir('../..')
    os.chdir('Linux-x86_64-RELEASE/')
    subprocess.run(['mkdir', os.path.join(openmvg_path, out_folder_name, 'stereo_vision')])
    subprocess.run(['./openMVG_main_openMVG2openMVS', '-i', os.path.join(openmvg_path, out_folder_name, 'reconstruction_global', 'robust.bin'), 
                                                      '-d', os.path.join(openmvg_path, out_folder_name, 'stereo_vision'), 
                                                      '-o', os.path.join(openmvg_path, out_folder_name, 'stereo_vision', 'Scene.mvs')])

    os.environ["PATH"] += os.pathsep + "/media/data-huy/bin/OpenMVS" # TODO: change to the absolute path of the folder where the bin files of openMVS locate (the one that you specify when using openMVS)
    # os.environ["PATH"] += os.pathsep + "/opt/3dmodel/3D-Reconstruction/bin/OpenMVS" # TODO: change to the absolute path of the folder where the bin files of openMVS locate (the one that you specify when using openMVS)
    os.chdir(os.path.join('../..', out_folder_name, 'stereo_vision/'))
    self.update_state(state='PROGRESS',
                      meta={'step': "DENSIFY POINT CLOUD", 'progress': 4, 'total': 7})
    subprocess.run(['DensifyPointCloud', 'Scene.mvs', '-v', '4'])
    self.update_state(state='PROGRESS',
                      meta={'step': "RECONSTRUCT MESH", 'progress': 5, 'total': 7})
    subprocess.run(['ReconstructMesh', 'Scene_dense.mvs'])
    self.update_state(state='PROGRESS',
                      meta={'step': "TEXTURE MESH", 'progress': 6, 'total': 7})
    subprocess.run(['TextureMesh', 'Scene_dense_mesh.mvs', ''.join(['--resolution-level=', str(resolution_scale)])])

    time.sleep(3)
    for fname in os.listdir('.'):
        if fname != 'Scene_dense_mesh_texture.ply' and fname != 'Scene_dense_mesh_texture.png':
            os.remove(os.path.join('.', fname))
    os.chdir('..')
    shutil.rmtree('./matches/')
    shutil.rmtree('./reconstruction_global/')
    os.chdir('..')

    self.update_state(state='PROGRESS',
                      meta={'step': "PREPARING FILE FOR DOWNLOAD", 'progress': 7, 'total': 7})
    end_time = time.time()
    hours, rem = divmod(end_time - start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print("[+] Execution time: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

    zipf = zipfile.ZipFile("".join([out_folder_name, '.zip']), 'w', zipfile.ZIP_DEFLATED)
    zipdir(out_folder_name, zipf)
    zipf.close()
    shutil.rmtree("".join(["./", out_folder_name]), ignore_errors=True)

    os.chdir('data')
    shutil.rmtree("".join(["./", images_folder_name]), ignore_errors=True)
    os.chdir(cwd)

    return {'step': "RETURN OUTPUT FILE", 'progress': 100, 'total': 100, 
            'output_file': "".join([out_folder_name, '.zip'])}