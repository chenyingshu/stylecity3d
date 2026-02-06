'''
Copyright (c) 2023 Yuseung Lee
Licensed under MIT License

Copyright (C) 2024 HKUST VGD Group
Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
'''

import numpy as np
import torch

def seed_everything(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def rotate_x(angle):
    r_mat = np.identity(3)
    sin_a = np.sin(angle)
    cos_a = np.cos(angle)
    r_mat[1, 1] = cos_a
    r_mat[2, 2] = cos_a
    r_mat[1, 2] = -sin_a
    r_mat[2, 1] = sin_a
    return r_mat

def rotate_y(angle):
    r_mat = np.identity(3)
    sin_a = np.sin(angle)
    cos_a = np.cos(angle)
    r_mat[0, 0] = cos_a
    r_mat[2, 2] = cos_a
    r_mat[0, 2] = sin_a
    r_mat[2, 0] = -sin_a
    return r_mat

def init_perspective_image_cor(fov_h=90, fov_v=90, num_sample_h=64, num_sample_v=64):
    fov_h = fov_h/180*np.pi
    fov_v = fov_v/180*np.pi
    # initi tangent image
    len_x = np.tan(fov_h/2)
    len_y = np.tan(fov_v/2)
    if num_sample_v is None:
        num_sample_v = int(num_sample_h * (fov_v / fov_h))
    cx, cy = np.meshgrid(np.linspace(-len_x, len_x, num_sample_h), np.linspace(-len_y, len_y, num_sample_v))
    xyz = np.concatenate([cx[..., None], cy[..., None], np.ones_like(cx)[..., None]], axis=-1)
    return xyz


def get_view_omni(omni_height, omni_width, window_size=64, stride=8):
    omni_height /= 8
    omni_width /= 8
    # num_blocks_height = (omni_height - window_size) // stride + 1
    # num_blocks_width = (omni_width - window_size) // stride + 1
    fx = omni_width / (2 * np.pi)
    fy = -omni_height / np.pi
    cx = omni_width / 2
    cy = omni_height / 2

    # init a plane/array [64, 64]
    ray = init_perspective_image_cor()
    views = []
    # sample in the sphere
    # assume one image per 45 deg
    num_sample = 16
    c_lats = np.linspace(0, np.pi/4, 4)
    c_lons = np.linspace(-np.pi, np.pi, num_sample)
    for c_lat in c_lats:
        for c_lon in c_lons:
            # get the rotation
            R = rotate_y(c_lon)  @ rotate_x(c_lat)
            dirs =  ray @ R.transpose()

            lon = np.arctan2(dirs[..., 0], dirs[..., 2])
            lat = np.arctan2(-dirs[..., 1], np.sqrt(dirs[..., 0]**2 + dirs[..., 2]**2)) 
            u = lon * fx + cx #- 0.5
            v = lat * fy + cy #- 0.5
            u = u.astype(np.int32)%(omni_width)
            v = v.astype(np.int32)%(omni_height)

            grid_x = lon / np.pi
            grid_y = -lat / (np.pi * 0.5)
            grid_xy = np.concatenate([grid_x[..., None], grid_y[..., None]], axis=-1).astype(np.float32)
            views.append({"u":u,
                        "v":v,
                        "grid_xy":grid_xy
                        })
    return views


def get_views(panorama_height, panorama_width, window_size=64, stride=8, loop_closure=False):
    panorama_height /= 8
    panorama_width /= 8
    num_blocks_height = (panorama_height - window_size) // stride + 1
    num_blocks_width = (panorama_width - window_size) // stride + 1
    total_num_blocks = int(num_blocks_height * num_blocks_width)
    views = []
    for i in range(total_num_blocks):
        h_start = int((i // num_blocks_width) * stride)
        h_end = h_start + window_size
        w_start = int((i % num_blocks_width) * stride)
        w_end = w_start + window_size
        views.append((h_start, h_end, w_start, w_end))

    if loop_closure:
        # NOTE: Only when height is (8 * window_size)
        assert panorama_height == window_size

        for i in range(window_size // stride - 2):
            h_start = 0
            h_end = window_size
            w_start = int(panorama_width - window_size + (i + 1) * stride)
            w_end = (i + 1) * stride
            views.append((h_start, h_end, w_start, w_end))

    return views


def set_latent_view(latent, h_start, h_end, w_start, w_end):
    '''Set the latent for each window'''
    if w_end > w_start:
        latent_view = latent[:, :, h_start:h_end, w_start:w_end].detach()
    else:
        latent_view = latent[:, :, h_start:h_end, w_start:]
        latent_view = torch.cat([
            latent_view,
            latent[:, :, h_start:h_end, :w_end]
        ], dim=-1)

    return latent_view


def exponential_decay_list(init_weight, decay_rate, num_steps):
    weights = [init_weight * (decay_rate ** i) for i in range(num_steps)]
    return torch.tensor(weights)