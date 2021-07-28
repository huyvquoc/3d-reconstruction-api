cd ./openMVG_Build/software/SfM
python SfM_GlobalPipeline.py "/media/data-huy/3D_Reconstruction/Github/openMVG/data/images" "/media/data-huy/3D_Reconstruction/Github/openMVG/output_images"
cd ../..
cd Linux-x86_64-RELEASE/
mkdir "/media/data-huy/3D_Reconstruction/Github/openMVG/output_images/stereo_vision"
./openMVG_main_openMVG2openMVS -i "/media/data-huy/3D_Reconstruction/Github/openMVG/output_images/reconstruction_global/robust.bin" -d "/media/data-huy/3D_Reconstruction/Github/openMVG/output_images/stereo_vision" -o "/media/data-huy/3D_Reconstruction/Github/openMVG/output_images/stereo_vision/Scene.mvs"
export PATH="/media/data-huy/bin/OpenMVS:$PATH"
cd ../../output_images/stereo_vision/
DensifyPointCloud Scene.mvs
ReconstructMesh Scene_dense.mvs
TextureMesh Scene_dense_mesh.mvs --resolution-level=3







