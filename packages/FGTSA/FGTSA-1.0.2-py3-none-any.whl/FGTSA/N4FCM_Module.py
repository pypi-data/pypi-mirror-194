import copy
import os
import re
from copy import deepcopy
from pathlib import Path

import numpy as np
import SimpleITK as sitk
import torchio as tio
from cv2 import fastNlMeansDenoising
from scipy.ndimage import binary_fill_holes
from skimage import measure

# ANCHOR const var
EPS = 1e-07
ALGORITHEM = 'FCM'
NUM_BIT = 16
NUM_CLUSTER = 3
FUZZINESS = 2
MAX_ITERATIONS = 50
EPSILON = 0.05


# ANCHOR functions

def get_breast_box(mask_array):
    mask_voxel_coords = np.where(mask_array)
    minzidx = int(np.min(mask_voxel_coords[0]))
    maxzidx = int(np.max(mask_voxel_coords[0])) + 1
    minxidx = int(np.min(mask_voxel_coords[1]))
    maxxidx = int(np.max(mask_voxel_coords[1])) + 1
    bbox = [[minzidx, maxzidx], [minxidx, maxxidx]]
    resizer = (slice(bbox[0][0], bbox[0][1]), slice(bbox[1][0], bbox[1][1]))
    return resizer

def get_breast_box_3d(mask_array, if_64=False):
    mask_voxel_coords = np.where(mask_array)
    mindidx = int(np.min(mask_voxel_coords[0]))
    maxdidx = int(np.max(mask_voxel_coords[0])) + 1
    minhidx = int(np.min(mask_voxel_coords[1]))
    maxhidx = int(np.max(mask_voxel_coords[1])) + 1
    minwidx = int(np.min(mask_voxel_coords[2]))
    maxwidx = int(np.max(mask_voxel_coords[2])) + 1

    #! 保证 y轴尺寸 大于 patch-size(64)
    if if_64:
        diff = maxhidx - minhidx
        print(f'[H] diff -> ({diff})')
        if diff <= 64:
            ep = int((64 - diff) / 2 + 2)
            maxhidx += ep
            minhidx -= ep
        print(f'[H] diff -> ({maxhidx - minhidx})')
    bbox = [[mindidx, maxdidx], [minhidx, maxhidx], [minwidx, maxwidx]]
    resizer = (slice(bbox[0][0], bbox[0][1]), slice(bbox[1][0], bbox[1][1]), slice(bbox[2][0], bbox[2][1]))
    return resizer

class FCM:
    def __init__(self, image, image_bit, n_clusters, m, epsilon, max_iter):
        '''Modified Fuzzy C-means clustering

        <image>: 2D array, grey scale image.
        <n_clusters>: int, number of clusters/segments to create.
        <m>: float > 1, fuzziness parameter. A large <m> results in smaller
             membership values and fuzzier clusters. Commonly set to 2.
        <max_iter>: int, max number of iterations.
        '''

        #-------------------Check inputs-------------------
        if np.ndim(image) != 2:
            raise Exception("<image> needs to be 2D (gray scale image).")
        if n_clusters <= 0 or n_clusters != int(n_clusters):
            raise Exception("<n_clusters> needs to be positive integer.")
        if m < 1:
            raise Exception("<m> needs to be >= 1.")
        if epsilon <= 0:
            raise Exception("<epsilon> needs to be > 0")

        self.image = image
        self.image_bit = image_bit
        self.n_clusters = n_clusters
        self.m = m
        self.epsilon = epsilon
        self.max_iter = max_iter

        self.shape = image.shape # image shape
        self.X = image.flatten().astype('float') # flatted image shape: (number of pixels,1)
        self.numPixels = image.size

    #---------------------------------------------
    def initial_U(self):
        U=np.zeros((self.numPixels, self.n_clusters))
        idx = np.arange(self.numPixels)
        # 超哥的初始化方法
        # U[0:int(self.numPixels/3),0]=1
        # U[int(self.numPixels/3):int(self.numPixels/3)*2,1]=1
        # U[int(self.numPixels/3)*2:self.numPixels,2]=1

        # 原初始化方法
        for ii in range(self.n_clusters):
            idxii = idx%self.n_clusters==ii
            U[idxii,ii] = 1
        return U

    def update_U(self):
        '''Compute weights'''
        c_mesh,idx_mesh = np.meshgrid(self.C,self.X)
        power = 2./(self.m-1)
        p1 = abs(idx_mesh-c_mesh)**power
        p2 = np.sum((1./(abs(idx_mesh-c_mesh)+ EPSILON)**power),axis=1)

        return 1./(p1*p2[:,None] + EPSILON)

    def update_C(self):
        '''Compute centroid of clusters'''
        numerator = np.dot(self.X,self.U**self.m)
        denominator = np.sum(self.U**self.m,axis=0)
        return numerator/denominator

    def form_clusters(self):
        '''Iterative training'''
        d = 100
        self.U = self.initial_U()
        if self.max_iter != -1:
            i = 0
            while True:
                self.C = self.update_C()
                old_u = np.copy(self.U)
                self.U = self.update_U()
                d = np.sum(abs(self.U - old_u))
                # print("Iteration %d : cost = %f" %(i, d))

                if d < self.epsilon or i > self.max_iter:
                    break
                i+=1
        else:
            i = 0
            while d > self.epsilon:
                self.C = self.update_C()
                old_u = np.copy(self.U)
                self.U = self.update_U()
                d = np.sum(abs(self.U - old_u))
                # print("Iteration %d : cost = %f" %(i, d))

                if d < self.epsilon or i > self.max_iter:
                    break
                i+=1
        self.segmentImage()


    def deFuzzify(self):
        return np.argmax(self.U, axis = 1)

    def segmentImage(self):
        '''Segment image based on max weights'''

        result = self.deFuzzify()
        self.result = result.reshape(self.shape).astype('int')

        return self.result

def get_result(img_arr):
    # --------------Clustering--------------
    algorithm = ALGORITHEM
    result = None
    if algorithm == 'FCM':
        cluster = FCM(img_arr, image_bit=NUM_BIT, n_clusters=NUM_CLUSTER, m=FUZZINESS, epsilon=EPSILON, max_iter=MAX_ITERATIONS)
        cluster.form_clusters()
        result=cluster.result
    else:
        raise Exception('There is a incorrect algorithm.')

    # --------------Pixel value standardizing--------------
    Ap_mask = copy.deepcopy(result)
    Bp_mask = copy.deepcopy(result)
    Cp_mask = copy.deepcopy(result)

    Ap_mask[Ap_mask != 0] = 1
    Ap_mask = 1 - Ap_mask

    Bp_mask[Bp_mask != 1] = 0

    Cp_mask[Cp_mask != 2] = 0
    Cp_mask[Cp_mask == 2] = 1

    Apart = img_arr * Ap_mask
    Bpart = img_arr * Bp_mask
    Cpart = img_arr * Cp_mask


    part_tuple = [
        [Ap_mask, Apart],
        [Bp_mask, Bpart],
        [Cp_mask, Cpart]
    ]

    background_, fat_, gland_ = sorted(part_tuple, key=lambda part_: part_[1].sum() / (part_[1][part_[1]>0].size + EPSILON))

    final_mask = gland_[0]

    return final_mask

def FCM_process(img_nparr, origin_shape, box_size):
    fcm_result = get_result(img_nparr)
    entry_mask = np.zeros(origin_shape, dtype=np.int16)
    entry_mask[box_size] = fcm_result
    return entry_mask

def denoising(raw_image, res_path=None):
    # :: 取CI
    max_value = np.percentile(raw_image, 99.8)
    # min_value = np.percentile(raw_image, 5)
    
    raw_image[raw_image > max_value] = max_value
    # raw_image[raw_image < min_value] = min_value
    raw_image = raw_image.astype(np.float32)
    # :: 在slice 2d 上操作denoising
    denoising_raw_stack = []
    print('Denoising...')
    for s2dm in raw_image:
        if s2dm.max() <= 0:
            print('Invalid Slice')
            denoising_raw_stack.append(s2dm)
        else:
            s2dm *= (255.0 / s2dm.max())  # ! raw MRI 需要normalization到 0 ~ 255
            s2dm = np.uint8(s2dm)
            dn_s2d = fastNlMeansDenoising(s2dm, None, 27, 7, 21)    # ? 15倍denoise
            denoising_raw_stack.append(dn_s2d)
            pass

    dn_3d_raw = np.stack(denoising_raw_stack, axis=0)
    print('Denoising RAW-MRI <* Get! *>')
    if res_path is not None:
        dn_3d_raw_img = sitk.GetImageFromArray(dn_3d_raw.astype(np.float32))
        sitk.WriteImage(dn_3d_raw_img, res_path)
        return dn_3d_raw_img

    return dn_3d_raw

def n4_trans(image_in, mask_in, out=None):
    image_ = sitk.Cast(sitk.GetImageFromArray(image_in), sitk.sitkFloat32)
    mask_ = sitk.Cast(sitk.GetImageFromArray(mask_in), sitk.sitkUInt8)
    n4_corrector = sitk.N4BiasFieldCorrectionImageFilter()
    # n4_corrector.SetMaximumNumberOfIterations((4,100))
    res = n4_corrector.Execute(image_, mask_)
    if out is not None:
        sitk.WriteImage(res, out)
    # print(f'N4 Done...')
    return sitk.GetArrayFromImage(res)

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

    return mpf

def max_connected_domain_process(origin_img_nparr, output=None):
    d, w, h = origin_img_nparr.shape
    layer_nparr = np.zeros((d, w, h)).astype(np.int16)

    #填充内部小孔
    for i in range(d):
        slices = origin_img_nparr[i, :, :]
        fillholes = binary_fill_holes(slices)
        layer_nparr[i, :, :] = fillholes

    #保留最大联通域
    area_box = []
    [region_labels, num] = measure.label(layer_nparr, return_num=True)
    region_prop = measure.regionprops(region_labels)

    for r in range(num):
        area_box.append(region_prop[r].area)

    max_region_label = area_box.index(max(area_box)) + 1

    region_labels[region_labels != max_region_label] = 0
    region_labels[region_labels == max_region_label] = 1
    max_connected_domain_img = np.array(region_labels, dtype=np.int8)

    if output is not None:
        max_connected_domain_sitk_img = sitk.GetImageFromArray(max_connected_domain_img)
        sitk.WriteImage(max_connected_domain_sitk_img, output)

    return max_connected_domain_img

def get_seg_res(image_arr):
    slice_result_list = []
    for slice_2d in image_arr:
        left_breast_2d_nparr, right_breast_2d_nparr = np.array_split(slice_2d, 2, axis=1)
        left_shape = left_breast_2d_nparr.shape
        right_shape = right_breast_2d_nparr.shape

        if left_breast_2d_nparr.sum() != 0:
            left_box_size = get_breast_box(left_breast_2d_nparr)
            left_box_region = left_breast_2d_nparr[left_box_size]
            left_part_2d_result = FCM_process(left_box_region, left_shape, left_box_size)
        else:
            left_part_2d_result = left_breast_2d_nparr

        if right_breast_2d_nparr.sum() != 0:
            right_box_size = get_breast_box(right_breast_2d_nparr)
            right_box_region = right_breast_2d_nparr[right_box_size]
            right_part_2d_result = FCM_process(right_box_region, right_shape, right_box_size)
        else:
            right_part_2d_result = right_breast_2d_nparr

        slice_result = np.hstack((left_part_2d_result, right_part_2d_result))
        slice_result_list.append(slice_result)
        pass

    seg_res_ = np.stack(slice_result_list, axis=0)

    return seg_res_


def fcm_processing(image_path: Path, dst_path: Path=None) -> np.ndarray:
    in_image_np = sitk.GetArrayFromImage(sitk.ReadImage(os.fspath(image_path)))
    
    # :: FCM seg processing
    fcm_seg_res = get_seg_res(in_image_np)
    
    if dst_path is not None:
        sitk.WriteImage(sitk.GetImageFromArray(fcm_seg_res), os.fspath(dst_path))
        
    return fcm_seg_res
