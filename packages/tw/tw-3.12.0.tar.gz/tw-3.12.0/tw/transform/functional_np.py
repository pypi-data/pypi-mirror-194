# Copyright 2022 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Functional
"""
import math
import random
import typing
import functools
from enum import Enum

import cv2
import PIL
from PIL import Image
import numpy as np

import torch
import torchvision.transforms.functional as tvf
import torchvision.transforms as tvt

import tw
from tw import transform as T


#!<-----------------------------------------------------------------------------
#!< DATA TYPE CONVERSION
#!<-----------------------------------------------------------------------------


def to_float(inputs: np.ndarray, **kwargs) -> np.ndarray:
  """convert to float
  """
  if inputs.dtype == 'float32':
    return inputs
  return inputs.astype('float32')


def to_round_uint8(inputs: np.ndarray, **kwargs) -> np.ndarray:
  """convert to round uint8
  """
  return inputs.round().clip(0, 255).astype('uint8')


def to_data_range(inputs: np.ndarray, src_range, dst_range, **kwargs) -> np.ndarray:
  return inputs * (float(dst_range) / float(src_range))


def to_tensor(inputs: np.ndarray, scale=None, mean=None, std=None, **kwargs) -> np.ndarray:
  # mean = torch.tensor(mean) if mean is not None else None
  # std = torch.tensor(std) if std is not None else None

  if inputs.ndim == 3:
    m = torch.from_numpy(np.ascontiguousarray(inputs.transpose((2, 0, 1))))
  elif inputs.ndim == 2:
    m = torch.from_numpy(inputs)[None]
  elif inputs.ndim == 4:
    m = torch.from_numpy(np.ascontiguousarray(inputs.transpose((0, 3, 1, 2))))
  else:
    raise NotImplementedError(inputs.ndim)

  m = m.type(torch.FloatTensor)
  if scale is not None:
    m = m.float().div(scale)
  if mean is not None:
    m.sub_(torch.tensor(mean)[:, None, None])
  if std is not None:
    m.div_(torch.tensor(std)[:, None, None])
  return m


def to_pil(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return tvf.to_pil_image(to_round_uint8(inputs))


def to_numpy(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return inputs

#!<-----------------------------------------------------------------------------
#!< FLIP
#!<-----------------------------------------------------------------------------


def hflip(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return np.ascontiguousarray(inputs[:, ::-1, ...])


def vflip(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return np.ascontiguousarray(inputs[::-1, ...])


def flip(inputs: np.ndarray, mode, **kwargs) -> np.ndarray:
  if mode == 0:
    return inputs
  elif mode == 1:
    return np.flipud(np.rot90(inputs))
  elif mode == 2:
    return np.flipud(inputs)
  elif mode == 3:
    return np.rot90(inputs, k=3)
  elif mode == 4:
    return np.flipud(np.rot90(inputs, k=2))
  elif mode == 5:
    return np.rot90(inputs)
  elif mode == 6:
    return np.rot90(inputs, k=2)
  elif mode == 7:
    return np.flipud(np.rot90(inputs, k=3))

#!<-----------------------------------------------------------------------------
#!< ROTATE
#!<-----------------------------------------------------------------------------


def rotate(inputs: np.ndarray, angle, interpolation=T.RESIZE_MODE.BILINEAR, border_mode=T.BORDER_MODE.CONSTANT, border_value=0, **kwargs) -> np.ndarray:
  scale = 1.0
  shift = (0, 0)
  height, width = inputs.shape[:2]
  matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, scale)
  matrix[0, 2] += shift[0]
  matrix[1, 2] += shift[1]
  cv2.warpAffine(inputs,
                 M=matrix,
                 dsize=(width, height),
                 dst=inputs,
                 flags=T.RESIZE_MODE_TO_CV[interpolation],
                 borderMode=T.BORDER_MODE_TO_CV[border_mode],
                 borderValue=border_value)
  return inputs

#!<-----------------------------------------------------------------------------
#!< AFFINE
#!<-----------------------------------------------------------------------------

# def _apply_affine_flow_np(flow, theta=None, t_x=0, t_y=0, zoom=1.0, shear=1.0, phi=0.0, interpolation=cv2.INTER_LINEAR):

#   h, w = flow.shape[:2]

#   if theta is None:
#     theta = _generate_affine_theta(t_x, t_y, zoom, shear, phi)

#   # T is similar transform matrix
#   T = np.array([[1. / (w - 1.), 0., -0.5], [0., 1. / (h - 1.), -0.5],
#                 [0., 0., 1.]], np.float32)

#   T_inv = np.linalg.inv(T)

#   # theta is affine transformations in world coordinates, with origin at top
#   # left corner of pictures and picture's width range and height range
#   # from [0, width] and [0, height].
#   theta_world = T_inv @ theta @ T

#   flow = cv2.warpAffine(flow, theta_world[:2, :], (w, h), flags=interpolation)

#   """
#   X1                 Affine(theta1)             X1'
#               x                                   x
#   theta1(-1) y           ->                      y
#               1                                   1

#   X2                 Affine(theta2)             X2'
#               x   u                                         x   u
#   theta1(-1) y + v       ->           theta2 x {theta1(-1) y + v}
#               1   0                                         1   0
#                                       flow' = X2' -X1'
#   """

#   # (u, v) -> (u, v, 0); shape (height, width, 2) -> (height, width, 3)
#   homo_flow = np.concatenate((flow, np.zeros((height, width, 1))), axis=2)

#   xx, yy = np.meshgrid(range(width), range(height))

#   # grid of homogeneous coordinates
#   homo_grid = np.stack((xx, yy, np.ones((height, width))), axis=2).astype(flow.dtype)

#   # theta2 x [u, v, 0]T + (theta2 x theta1(-1) - [1, 1, 1]) x [x, y, 1]T
#   flow_final = homo_grid @ (theta2 @ np.linalg.inv(theta1) - np.eye(3)).T + homo_flow @ theta2.T

#   return flow_final[:, :, :2]


def _generate_random_affine_theta(translates, zoom, shear, rotate, preserve_valid):
  """A valid affine transform is an affine transform which guarantees the
    transformed image covers the whole original picture frame.
  """
  def is_valid(theta):
    bounds = np.array([
        [-0.5, -0.5, 1.],  # left top
        [-0.5, 0.5, 1.],  # left bottom
        [0.5, -0.5, 1.],  # right top
        [0.5, 0.5, 1.],  # right bottom
    ])
    """
    (-0.5, -0.5)          (0.5, -0.5)
                 --------
                |        |
                |        |
                |        |
                 --------
    (-0.5, 0.5)          (0.5, 0.5)
    """
    bounds = (np.linalg.inv(theta) @ bounds.T).T

    valid = ((bounds[:, :2] >= -0.5) & (bounds[:, :2] <= 0.5)).all()
    return valid

  valid = False
  theta = np.identity(3)

  while not valid:
    zoom_ = np.random.uniform(zoom[0], zoom[1])
    shear_ = np.random.uniform(shear[0], shear[1])
    t_x = np.random.uniform(-translates[0], translates[0])
    t_y = np.random.uniform(-translates[1], translates[1])
    phi = np.random.uniform(rotate[0] * np.pi / 180., rotate[1] * np.pi / 180.)
    T = _generate_affine_theta(t_x, t_y, zoom_, shear_, phi)
    theta_propose = T @ theta
    if not preserve_valid:
      break
    valid = is_valid(theta_propose)

  return theta_propose


def _generate_affine_theta(t_x, t_y, zoom, shear, phi):
  """generate a affine matrix
  """
  sin_phi = np.sin(phi)
  cos_phi = np.cos(phi)

  translate_mat = np.array([
      [1., 0., t_x],
      [0., 1., t_y],
      [0., 0., 1.],
  ])

  rotate_mat = np.array([
      [cos_phi, -sin_phi, 0.],
      [sin_phi, cos_phi, 0.],
      [0., 0., 1.],
  ])

  shear_mat = np.array([
      [shear, 0., 0.],
      [0., 1. / shear, 0.],
      [0., 0., 1.],
  ])

  zoom_mat = np.array([
      [zoom, 0., 0.],
      [0., zoom, 0.],
      [0., 0., 1.],
  ])

  T = translate_mat @ rotate_mat @ shear_mat @ zoom_mat
  return T


def affine_theta(inputs: np.ndarray, theta, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs) -> np.ndarray:
  # T is similar transform matrix
  h, w = inputs.shape[:2]
  trans = np.array([[1. / (w - 1.), 0., -0.5], [0., 1. / (h - 1.), -0.5], [0., 0., 1.]], np.float32)

  trans_inv = np.linalg.inv(trans)

  # theta is affine transformations in world coordinates, with origin at top
  # left corner of pictures and picture's width range and height range
  # from [0, width] and [0, height].
  theta_world = trans_inv @ theta @ trans

  return cv2.warpAffine(inputs, theta_world[:2, :], (w, h), flags=T.RESIZE_MODE_TO_CV[interpolation])

def affine(inputs: np.ndarray, angle: float, tx: float, ty: float, scale: float, shear: float, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs) -> np.ndarray:
  theta = _generate_affine_theta(tx, ty, scale, shear, angle)
  return affine_theta(inputs, theta, interpolation=interpolation, **kwargs)


#!<-----------------------------------------------------------------------------
#!< COLORSPACE
#!<-----------------------------------------------------------------------------

def change_colorspace(inputs: np.ndarray, src: T.COLORSPACE, dst: T.COLORSPACE, **kwargs) -> np.ndarray:

  if src == T.COLORSPACE.BGR and dst == T.COLORSPACE.RGB:
    return cv2.cvtColor(inputs, cv2.COLOR_BGR2RGB)
  elif src == T.COLORSPACE.RGB and dst == T.COLORSPACE.BGR:
    return cv2.cvtColor(inputs, cv2.COLOR_RGB2BGR)

  elif src == T.COLORSPACE.RGB and dst == T.COLORSPACE.HSV:
    return cv2.cvtColor(inputs, cv2.COLOR_RGB2HSV)
  elif src == T.COLORSPACE.HSV and dst == T.COLORSPACE.RGB:
    return cv2.cvtColor(inputs, cv2.COLOR_HSV2RGB)

  elif src == T.COLORSPACE.RGB and dst == T.COLORSPACE.YUV709F:
    return rgb_to_yuv709f(inputs)
  elif src == T.COLORSPACE.RGB and dst == T.COLORSPACE.YUV709V:
    return rgb_to_yuv709v(inputs)
  elif src == T.COLORSPACE.RGB and dst == T.COLORSPACE.YUV601F:
    return rgb_to_yuv601(inputs)
  elif src == T.COLORSPACE.RGB and dst == T.COLORSPACE.YUV601V:
    return rgb_to_yuv601(inputs)

  elif src == T.COLORSPACE.YUV709F and dst == T.COLORSPACE.RGB:
    return yuv709f_to_rgb(inputs)
  elif src == T.COLORSPACE.YUV709V and dst == T.COLORSPACE.RGB:
    return yuv709v_to_rgb(inputs)
  elif src == T.COLORSPACE.YUV601F and dst == T.COLORSPACE.RGB:
    return yuv601_to_rgb(inputs)
  elif src == T.COLORSPACE.YUV601V and dst == T.COLORSPACE.RGB:
    return yuv601_to_rgb(inputs)

  raise NotImplementedError


def to_color(inputs: np.ndarray, **kwargs) -> np.ndarray:
  if inputs.ndim == 3 and inputs.shape[2] == 3:
    return inputs
  h, w = inputs.shape[:2]
  inputs = inputs.reshape([h, w, 1])
  return np.repeat(inputs, 3, axis=2)


def to_grayscale(inputs: np.ndarray, **kwargs) -> np.ndarray:
  h, w = inputs.shape[:2]
  if inputs.ndim == 3 and inputs.shape[2] != 1:
    return np.mean(inputs, axis=2, keepdims=True)
  elif inputs.ndim == 2:
    return inputs.reshape(h, w, 1)


def rgb_to_yuv709v(inputs: np.ndarray, **kwargs) -> np.ndarray:
  R, G, B = np.split(inputs, 3, axis=2)
  Y = 0.1826 * R + 0.6142 * G + 0.0620 * B + 16  # [16, 235]
  U = -0.1007 * R - 0.3385 * G + 0.4392 * B + 128  # [16, 240]
  V = 0.4392 * R - 0.3990 * G - 0.0402 * B + 128  # [16, 240]
  return np.concatenate([Y, U, V], axis=2)


def rgb_to_yuv709f(inputs: np.ndarray, **kwargs) -> np.ndarray:
  R, G, B = np.split(inputs, 3, axis=2)
  Y = 0.2126 * R + 0.7152 * G + 0.0722 * B  # [0, 255]
  U = -0.1146 * R - 0.3854 * G + 0.5000 * B + 128  # [0, 255]
  V = 0.5000 * R - 0.4542 * G - 0.0468 * B + 128  # [0, 255]
  return np.concatenate([Y, U, V], axis=2)


def yuv709v_to_rgb(inputs: np.ndarray, **kwargs) -> np.ndarray:
  Y, U, V = np.split(inputs, 3, axis=2)
  Y = Y - 16
  U = U - 128
  V = V - 128
  R = 1.1644 * Y + 1.7927 * V
  G = 1.1644 * Y - 0.2132 * U - 0.5329 * V
  B = 1.1644 * Y + 2.1124 * U
  return np.concatenate([R, G, B], axis=2)


def yuv709f_to_rgb(inputs: np.ndarray, **kwargs) -> np.ndarray:
  Y, U, V = np.split(inputs, 3, axis=2)
  Y = Y
  U = U - 128
  V = V - 128
  R = 1.000 * Y + 1.570 * V
  G = 1.000 * Y - 0.187 * U - 0.467 * V
  B = 1.000 * Y + 1.856 * U
  return np.concatenate([R, G, B], axis=2)


def rgb_to_bgr(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return cv2.cvtColor(inputs, cv2.COLOR_RGB2BGR)


def bgr_to_rgb(inputs: np.ndarray, **kwargs) -> np.ndarray:
  return cv2.cvtColor(inputs, cv2.COLOR_RGB2BGR)


def rgb_to_yuv601(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def yuv601_to_rgb(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def rgb_to_yiq(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def rgb_to_lhm(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def rgb_to_xyz(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def xyz_to_lab(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def rgb_to_lab(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


#!<-----------------------------------------------------------------------------
#!< PHOTOMETRIC
#!<-----------------------------------------------------------------------------

def adjust_sharpness(inputs: np.ndarray, factor, **kwargs) -> np.ndarray:
  raise NotImplementedError


def adjust_brightness(inputs: np.ndarray, factor, **kwargs) -> np.ndarray:
  raise NotImplementedError


def adjust_contrast(inputs: np.ndarray, factor, **kwargs) -> np.ndarray:
  raise NotImplementedError


def adjust_gamma(inputs: np.ndarray, factor, gain, **kwargs) -> np.ndarray:
  raise NotImplementedError


def adjust_hue(inputs: np.ndarray, factor, **kwargs) -> np.ndarray:
  raise NotImplementedError


def adjust_saturation(inputs: np.ndarray, factor, **kwargs) -> np.ndarray:
  raise NotImplementedError


def photometric_distortion(inputs: np.ndarray,
                           brightness_delta=32,
                           contrast_range=(0.5, 1.5),
                           saturation_range=(0.5, 1.5),
                           hue_delta=18,
                           **kwargs) -> np.ndarray:
  # random brightness
  if random.randint(0, 2):
    delta = random.uniform(-brightness_delta, brightness_delta)
    inputs += delta

  # mode == 0 --> do random contrast first
  # mode == 1 --> do random contrast last
  mode = random.randint(0, 2)
  if mode == 1:
    if random.randint(0, 2):
      alpha = random.uniform(contrast_range[0], contrast_range[1])
      inputs *= alpha

  # convert color from BGR to HSV
  inputs = change_colorspace(inputs, src=T.COLORSPACE.RGB, dst=T.COLORSPACE.HSV)

  # random saturation
  if random.randint(0, 2):
    inputs[..., 1] *= random.uniform(saturation_range[0], saturation_range[1])

  # random hue
  if random.randint(0, 2):
    inputs[..., 0] += random.uniform(-hue_delta, hue_delta)
    inputs[..., 0][inputs[..., 0] > 360] -= 360
    inputs[..., 0][inputs[..., 0] < 0] += 360

  # convert color from HSV to BGR
  inputs = change_colorspace(inputs, src=T.COLORSPACE.HSV, dst=T.COLORSPACE.RGB)

  # random contrast
  if mode == 0:
    if random.randint(0, 2):
      alpha = random.uniform(contrast_range[0], contrast_range[1])
      inputs *= alpha

  # randomly swap channels
  if random.randint(0, 2):
    axis = [0, 1, 2]
    random.shuffle(axis)
    inputs = inputs[..., axis]

  return inputs

#!<-----------------------------------------------------------------------------
#!< CROP
#!<-----------------------------------------------------------------------------


def crop(inputs: np.ndarray, top, left, height, width, **kwargs) -> np.ndarray:
  return inputs[top: top + height, left: left + width]


def center_crop(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def center_crop_and_pad(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def resized_crop(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def ten_crop(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def five_crop(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def non_overlap_crop_patch(inputs: np.ndarray, patch_size=32, stride=32, **kwargs) -> np.ndarray:
  h, w = inputs.shape[:2]
  patches = []
  for y in range(0, h - stride, stride):
    for x in range(0, w - stride, stride):
      patch = inputs[y: y + patch_size, x: x + patch_size]
      patches.append(patch)
  inputs = np.stack(patches, axis=0).to(inputs)
  return inputs

#!<-----------------------------------------------------------------------------
#!< FILTER
#!<-----------------------------------------------------------------------------


def iso_noise(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def gaussian_noise(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def gaussian_blur(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def motion_blur(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def median_blur(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def sobel(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError

#!<-----------------------------------------------------------------------------
#!< MORPHOLOGY
#!<-----------------------------------------------------------------------------


def alpha_to_trimap(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError

#!<-----------------------------------------------------------------------------
#!< NORMALIZE
#!<-----------------------------------------------------------------------------


def equal_hist(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def truncated_standardize(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def local_contrast_normalize(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError

#!<-----------------------------------------------------------------------------
#!< PADDING
#!<-----------------------------------------------------------------------------


def pad(inputs: np.ndarray, left, top, right, bottom, fill_value=0, mode='constant', **kwargs) -> np.ndarray:
  if inputs.ndim == 3:
    inputs = np.pad(inputs, ((top, bottom), (left, right), (0, 0)), mode=mode, constant_values=fill_value)
  elif inputs.ndim == 2:
    inputs = np.pad(inputs, ((top, bottom), (left, right)), mode=mode, constant_values=fill_value)
  return inputs


def crop_and_pad(inputs: np.ndarray,
                 src_crop_y,
                 src_crop_x,
                 src_crop_h,
                 src_crop_w,
                 dst_crop_y,
                 dst_crop_x,
                 dst_height,
                 dst_width,
                 fill_value=0,
                 mode='constant',
                 **kwargs) -> np.ndarray:
  new_shape = list(inputs.shape)
  h, w = new_shape[:2]
  new_shape[0] = dst_height
  new_shape[1] = dst_width
  new_image = np.ones([*new_shape]).astype(inputs.dtype) * fill_value

  sy1 = max(src_crop_y, 0)
  sy2 = min(src_crop_y + src_crop_h, h)
  sx1 = max(src_crop_x, 0)
  sx2 = min(src_crop_x + src_crop_w, w)

  dy1 = max(dst_crop_y, 0)
  dy2 = min(dst_crop_y + src_crop_h, dst_height)
  dx1 = max(dst_crop_x, 0)
  dx2 = min(dst_crop_x + src_crop_w, dst_width)

  # actual crop size
  ch = min(dy2 - dy1, sy2 - sy1)
  cw = min(dx2 - dx1, sx2 - sx1)

  # update crop area
  sy2 = sy1 + ch
  sx2 = sx1 + cw
  dy2 = dy1 + ch
  dx2 = dx1 + cw

  new_image[dy1:dy2, dx1:dx2] = inputs[sy1:sy2, sx1:sx2]
  return new_image


def pad_to_size_divisible(inputs: np.ndarray, size_divisible, **kwargs) -> np.ndarray:
  shape = list(inputs.shape)
  shape[0] = int(math.ceil(shape[0] / size_divisible) * size_divisible)
  shape[1] = int(math.ceil(shape[1] / size_divisible) * size_divisible)
  outputs = np.zeros(shape).astype(inputs.dtype)
  outputs[:inputs.shape[0], :inputs.shape[1]] = inputs
  return outputs


def pad_to_square(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def pad_to_target_size(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError

#!<-----------------------------------------------------------------------------
#!< RESIZE
#!<-----------------------------------------------------------------------------


def shortside_resize(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError


def resize(inputs: np.ndarray, height, width, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs) -> np.ndarray:
  return cv2.resize(inputs, dsize=(width, height), interpolation=T.RESIZE_MODE_TO_CV[interpolation])


def adaptive_resize(inputs: np.ndarray, **kwargs) -> np.ndarray:
  raise NotImplementedError
