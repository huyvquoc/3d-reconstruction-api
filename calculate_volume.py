from pyntcloud import PyntCloud
import numpy as np


def signed_volume_of_triangle(v1, v2, v3):
    v321 = v3[0]*v2[1]*v1[2]
    v231 = v2[0]*v3[1]*v1[2]
    v312 = v3[0]*v1[1]*v2[2]
    v132 = v1[0]*v3[1]*v2[2]
    v213 = v2[0]*v1[1]*v3[2]
    v123 = v1[0]*v2[1]*v3[2]
    f1 = 1/6
    f2 = v231 - v321 + v312 - v132 + v123 - v213 
    return f1*f2

def volume_of_mesh(v1_list, v2_list, v3_list):
    vol_list = []
    n_tris = v1_list.shape[0]
    print('[++] The number of meshes: ', n_tris)
    for tris_id in range(n_tris):
        v1 = v1_list[tris_id]
        v2 = v2_list[tris_id]
        v3 = v3_list[tris_id]
        vol_list.append(signed_volume_of_triangle(v1, v2, v3))
    return sum(vol_list)


cloud = PyntCloud.from_file("./output_snackcan_global/stereo_vision/Scene_dense_mesh_texture.ply")

v1_list, v2_list, v3_list = cloud.get_mesh_vertices()
print("[++] Min of v1_list", np.amin(v1_list, axis=0))
print("[++] Max of v1_list", np.amax(v1_list, axis=0))
print("[++] Min of v2_list", np.amin(v2_list, axis=0))
print("[++] Max of v2_list", np.amax(v2_list, axis=0))
print("[++] Min of v3_list", np.amin(v3_list, axis=0))
print("[++] Max of v3_list", np.amax(v3_list, axis=0))
volume = abs(volume_of_mesh(v1_list, v2_list, v3_list))
print("[+] Volume: ", volume)