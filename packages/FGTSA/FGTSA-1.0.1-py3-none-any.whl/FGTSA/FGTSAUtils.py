import copy
import numpy as np
from scipy.ndimage import binary_fill_holes
from skimage import measure

# =================BPE Function================= #
def get_mid_part(nparr, mid_part=None, is_crop=False):
    if mid_part is None:
        mid_part = [0., 1.]
    d_dim = nparr.shape[0]
    if is_crop:
        mpf = nparr[int(d_dim * mid_part[0]):int(d_dim * mid_part[1]), :, :]
    else:
        nparr[:int(d_dim * mid_part[0]), :, :] = 0
        nparr[int(d_dim * mid_part[1]):, :, :] = 0
        mpf = nparr

    print(f'Get mid part {mid_part}')
    return mpf


def get_VbV_BPE(PE, gland_size):
    avg_bpe = PE / gland_size
    return round(avg_bpe, 7)

def get_MI_BPE(UnE_Gland, E_Gland, gland_size):
    UnE_Gland_Intensities = UnE_Gland.sum() / gland_size
    E_Gland_Intensities = E_Gland.sum() / gland_size
    
    Mean_Intensities_BPE = (E_Gland_Intensities - UnE_Gland_Intensities) / UnE_Gland_Intensities 
    return round(Mean_Intensities_BPE, 7)

def get_m95p_mask(ori_gland, ori_mask):
    gland = copy.deepcopy(ori_gland)
    gland_ = gland[ori_mask == 1]
    gland_.sort()
    index_ = gland_.size
    p2_5 = gland_[int(index_*0.025)-1]
    p97_5 = gland_[int(index_*0.975)-1]
    gland[gland<p2_5] = 0
    gland[gland>p97_5] = 0   
    gland[gland>0] = 1    
    return gland

def get_PE(UnE_Gland, E_Gland):
    voxel_PE = (E_Gland - UnE_Gland) / (UnE_Gland)
    
    voxel_PE[voxel_PE<0.1] = 0
    
    return voxel_PE

def get_BPE_volume(BPE, p_list):
    v_list = []
    for p in p_list:
        v = BPE[BPE>p].size
        v_list.append(v)
    
    return v_list

def get_glands_value(lg, rg, bg_mask):
    lm, rm = np.array_split(bg_mask, 2, axis=2)
    lv = lg[lm == 1]
    rv = rg[rm == 1]
    return lv, rv

# =================Function================= #
def get_breast_box_3d(mask_array, if_64=False):
    mask_voxel_coords = np.where(mask_array)
    mindidx = int(np.min(mask_voxel_coords[0]))
    maxdidx = int(np.max(mask_voxel_coords[0])) + 1
    minhidx = int(np.min(mask_voxel_coords[1]))
    maxhidx = int(np.max(mask_voxel_coords[1])) + 1
    minwidx = int(np.min(mask_voxel_coords[2]))
    maxwidx = int(np.max(mask_voxel_coords[2])) + 1

    if if_64:
        diff = maxhidx - minhidx
        if diff <= 64:
            print(f'[H] -> ({diff})')
            ep = int((64 - diff) / 2 + 2)
            maxhidx += ep
            minhidx -= ep
            print(f'Corrected [H] -> ({maxhidx - minhidx})')
    bbox = [[mindidx, maxdidx], [minhidx, maxhidx], [minwidx, maxwidx]]
    resizer = (slice(bbox[0][0], bbox[0][1]), slice(bbox[1][0], bbox[1][1]), slice(bbox[2][0], bbox[2][1]))
    return resizer

def max_connected_domain_process(origin_img_nparr):
    d, w, h = origin_img_nparr.shape
    layer_nparr = np.zeros((d, w, h)).astype(np.int16)

    for i in range(d):
        slices = origin_img_nparr[i, :, :]
        fillholes = binary_fill_holes(slices)
        layer_nparr[i, :, :] = fillholes

    area_box = []
    [region_labels, num] = measure.label(layer_nparr, return_num=True)
    region_prop = measure.regionprops(region_labels)

    for r in range(num):
        area_box.append(region_prop[r].area)

    max_region_label = area_box.index(max(area_box)) + 1

    region_labels[region_labels != max_region_label] = 0
    region_labels[region_labels == max_region_label] = 1


    return np.array(region_labels, dtype=np.int16)