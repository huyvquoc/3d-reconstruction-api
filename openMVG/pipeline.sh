python SfM_SequentialPipeline.py "/media/data-huy/3D Reconstruction/Github/Image_datasets/360_dataset/360_school/images" "/media/data-huy/3D Reconstruction/Github/openMVG/output"

python SfM_SequentialPipeline.py "/media/data-huy/3D Reconstruction/Github/openMVG/data/mug" "/media/data-huy/3D Reconstruction/Github/openMVG/output_mug"

python SfM_GlobalPipeline.py "/media/data-huy/3D_Reconstruction/Github/openMVG/data/mug_large" "/media/data-huy/3D_Reconstruction/Github/openMVG/output_mug_large"

python SfM_GlobalPipeline.py "/media/data-huy/3D_Reconstruction/Github/openMVG/data/snackcan" "/media/data-huy/3D_Reconstruction/Github/openMVG/output_snackcan_global"

cd ../..

cd Linux-x86_64-RELEASE/

./openMVG_main_openMVG2openMVS -i "/media/data-huy/3D_Reconstruction/Github/openMVG/output_snackcan_global/reconstruction_global/sfm_data.bin" -d "/media/data-huy/3D_Reconstruction/Github/openMVG/output_snackcan_global/stereo_vision" -o "/media/data-huy/3D_Reconstruction/Github/openMVG/output_snackcan_global/stereo_vision/Scene.mvs"

./openMVG_main_openMVG2openMVS -i "/media/data-huy/3D_Reconstruction/Github/openMVG/output_mug_large_sequential/reconstruction_sequential/sfm_data.bin" -d "/media/data-huy/3D_Reconstruction/Github/openMVG/output_mug_large_sequential/stereo_vision" -o "/media/data-huy/3D_Reconstruction/Github/openMVG/output_mug_large_sequential/stereo_vision/Scene.mvs"

Install openMVS

export PATH="/media/data-huy/bin/OpenMVS:$PATH"

cd output_mug_global

cd stereo_vision/

DensifyPointCloud Scene.mvs

ReconstructMesh Scene_dense.mvss

TextureMesh Scene_dense_mesh.mvs --resolution-level=3
