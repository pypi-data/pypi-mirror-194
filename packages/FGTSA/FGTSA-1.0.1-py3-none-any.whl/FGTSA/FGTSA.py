import os
import re
from pathlib import Path
import numpy as np
import pandas as pd
import SimpleITK as sitk
from scipy.ndimage import binary_fill_holes
from . import FGTSAUtils
from . import N4FCM_Module


def bias_field_correction_main(image_path: Path, out_path: Path=None) -> np.ndarray:
    image_np = sitk.GetArrayFromImage(sitk.ReadImage(os.fspath(image_path)))
    mask_np = deepcopy(image_np)
    mask_np[mask_np != 0] = 1
    cor_mask_np = binary_fill_holes(mask_np).astype(np.int8)
    n4_cor_img_np = n4_trans(image_in=image_np, mask_in=cor_mask_np)
    if out_path is not None:
        sitk.WriteImage(sitk.GetImageFromArray(n4_cor_img_np), os.fspath(out_path))
    return n4_cor_img_np


def fgt_seg_main(bfc_img_path: Path, seg_path: Path) -> np.ndarray:
    seg_res_np = fcm_processing(bfc_img_path, seg_path)
    return seg_res_np


def BPE_calc_main(c0_img_path:Path, peak_img_path:Path, lesion_csv_path:Path, seg_res_path:Path, bpr_csv_path:Path) -> pd.DataFrame:
    # * get info
    item = c0_img_path.name
    pid = re.findall('\d+', item)[-1]
    
    # * get lesion location info
    Location_pd = pd.read_csv(lesion_csv_path, index_col='ID')
    local_list = Location_pd.index.tolist()
    local_list = [str(x) for x in local_list]
    
    patient_BPE_info = [pid]
    patient_right_BPE_info = []
    patient_left_BPE_info = []
    Patient_BPE_Result_List = []
    
    # * get images numpy array
    C0_raw_np = sitk.ReadImage(sitk.GetArrayFromImage(os.fspath(c0_img_path)))
    C2_raw_np = sitk.ReadImage(sitk.GetArrayFromImage(os.fspath(peak_img_path)))
    
    # * get FGT mask numpy array
    origin_FGT_mask_np = sitk.GetArrayFromImage(sitk.ReadImage(os.fspath(seg_res_path)))
    FGT_mask_np = get_mid_part(origin_FGT_mask_np, mid_part=[0.25, 0.75])
    FGT_mask_np[FGT_mask_np > 0] = 1
    
    # * get mid 95% value gland mask (unenhanced c0 zero)
    m95p_C0_FGT_mask = get_m95p_mask(C0_raw_np * FGT_mask_np, FGT_mask_np)
    
    # * get FGT numpy array
    C0_FGT_np = C0_raw_np * m95p_C0_FGT_mask
    C2_FGT_np = C2_raw_np * m95p_C0_FGT_mask
    
    # * get left and right part FGT
    C0_right_FGT, C0_left_FGT = np.array_split(C0_FGT_np, 2, axis=2)
    C2_right_FGT, C2_left_FGT = np.array_split(C2_FGT_np, 2, axis=2)
    
    # * FGT numpy array flatten
    C0_right_value, C0_left_value = get_glands_value(C0_right_FGT, C0_left_FGT, m95p_C0_FGT_mask)
    C2_right_value, C2_left_value = get_glands_value(C2_right_FGT, C2_left_FGT, m95p_C0_FGT_mask)
    
    # * get FGT volume
    right_FGT_vol = m95p_C0_FGT_mask[:, :, :int(m95p_C0_FGT_mask.shape[2] / 2)].sum()
    left_FGT_vol = m95p_C0_FGT_mask[:, :, int(m95p_C0_FGT_mask.shape[2] / 2):].sum()
    
    # TODO: get PE and Voxel by Voxel BPE result
    C2_right_value_cp = copy.deepcopy(C2_right_value)
    C2_left_value_cp = copy.deepcopy(C2_left_value)
    
    right_PE = get_PE(C0_right_value, C2_right_value_cp)
    left_PE = get_PE(C0_left_value, C2_left_value_cp)
    
    right_side_VbVBPE = get_VbV_BPE(right_PE.sum(), right_FGT_vol)
    left_side_VbVBPE = get_VbV_BPE(left_PE.sum(), left_FGT_vol)
    
    # * get Voxel by Voxel BPE volume
    BPE_volume_right_list = get_BPE_volume(right_PE, [0.1, 0.25, 0.5, 0.75])
    BPE_volume_left_list = get_BPE_volume(left_PE, [0.1, 0.25, 0.5, 0.75])
    
    # * load results
    patient_right_BPE_info.extend([right_side_VbVBPE, *BPE_volume_right_list])
    patient_left_BPE_info.extend([left_side_VbVBPE, *BPE_volume_left_list])
    
    # * append Patient BPE Results
    patient_BPE_info.extend(patient_right_BPE_info)
    patient_BPE_info.extend(patient_left_BPE_info)
    
    # * get health side label and result
    if Location_pd['Position'][int(pid)] == 'R':
        patient_BPE_info.extend(['Left', left_side_VbVBPE])
        patient_BPE_info.extend(BPE_volume_left_list)
    elif Location_pd['Position'][int(pid)] == 'L':
        patient_BPE_info.extend(['Right', right_side_VbVBPE])
        patient_BPE_info.extend(BPE_volume_right_list)
        pass
    
    Patient_BPE_Result_List.append(patient_BPE_info)
    
    print('BPE Calculation Done!')
    print(f'# ====================={item} DONE! ====================== #')

    columns_set = ['Patient_ID', 
                'Right_Side_VbVBPE', 'R10perBPE_Volume', 'R25perBPE_Volume', 'R50perBPE_Volume', 'R75perBPE_Volume', 
                'Left_Side_VbVBPE', 'L10perBPE_Volume', 'L25perBPE_Volume', 'L50perBPE_Volume', 'L75perBPE_Volume', 
                'Health_Side',
                'Health_Side_VbVBPE', 'H10perBPE_Volume', 'H25perBPE_Volume', 'H50perBPE_Volume', 'H75perBPE_Volume']

    dt = pd.DataFrame(Patient_BPE_Result_List, columns=columns_set)

    if bpr_csv_path is not None:
        dt.to_csv(os.fspath(bpr_csv_path / "bpe_res.csv"), index=False)
    
    return dt