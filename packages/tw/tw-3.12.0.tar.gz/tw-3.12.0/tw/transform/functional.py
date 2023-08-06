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

from . import functional_np as F_np
from . import functional_pil as F_pil
from . import functional_tensor as F_t


def supports(support=[np.ndarray, Image.Image, torch.Tensor, T.MetaBase], *args, **kwargs):
  """Decorator for supplying meta actions.

    1. convert single meta into list of metas
    2. select user-specific meta index to augment
    3. checking if current augment to allow meta type pass.
    4. shape checking

  """
  def wrapper(transform):
    @functools.wraps(transform)
    def kernel(inputs, *args, **kwargs):
      # convert metabase to list
      if isinstance(inputs, T.MetaBase):
        inputs = [inputs]

      # allow class
      if len(support) > 0:
        # for [metabase, ]
        if isinstance(inputs, (list, tuple)):
          for inp in inputs:
            assert isinstance(inp, tuple(support)), f"Failed to find {type(inp)} in {support} on {transform}."
        else:
          assert isinstance(inputs, tuple(support)), f"Failed to find {type(inputs)} in {support} on {transform}."

      # check shape
      if isinstance(inputs, np.ndarray):
        assert inputs.ndim in [2, 3], "inputs should be [H, W], [H, W, C]."
      elif isinstance(inputs, torch.Tensor):
        assert inputs.ndim in [2, 3, 4], "inputs should be [B, C, H, W], [C, H, W], [H, W]"

      # there should not be metabase
      assert not isinstance(inputs, T.MetaBase)

      # doing for meta-class
      if isinstance(inputs, (list, tuple)):
        for meta in inputs:
          if hasattr(meta, transform.__name__):
            getattr(meta, transform.__name__)(*args, **kwargs)
          else:
            tw.logger.warn(f'{meta.__class__.__name__} does not implement {transform.__name__} method.')
        return default_return_meta(inputs, *args, **kwargs)

      return transform(inputs, *args, **kwargs)
    return kernel
  return wrapper


def default_return_meta(inputs, *args, **kwargs):
  return inputs


def get_inputs_hw(inputs):
  """get inputs h, w size
  """
  if isinstance(inputs, np.ndarray):
    h, w = inputs.shape[:2]
  elif isinstance(inputs, Image.Image):
    h, w = inputs.height, inputs.width
  elif isinstance(inputs, torch.Tensor):
    if inputs.ndim in [2, 3, 4, 5]:
      h, w = inputs.shape[-2:]
    else:
      raise NotImplementedError
  return h, w

#!<-----------------------------------------------------------------------------
#!< DATA TYPE CONVERSION
#!<-----------------------------------------------------------------------------


@supports()
def to_float(inputs, **kwargs):
  """convert to float
  """
  if isinstance(inputs, np.ndarray):
    return F_np.to_float(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.to_float(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.to_float(inputs, **kwargs)


@supports()
def to_round_uint8(inputs, **kwargs):
  """convert to round uint8
  """
  if isinstance(inputs, np.ndarray):
    return F_np.to_round_uint8(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.to_round_uint8(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.to_round_uint8(inputs, **kwargs)


@supports()
def to_data_range(inputs, src_range, dst_range, **kwargs):
  if src_range == dst_range:
    return inputs

  if isinstance(inputs, np.ndarray):
    return F_np.to_data_range(inputs, src_range=src_range, dst_range=dst_range, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.to_data_range(inputs, src_range=src_range, dst_range=dst_range, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.to_data_range(inputs, src_range=src_range, dst_range=dst_range, **kwargs)


@supports()
def to_tensor(inputs, scale=None, mean=None, std=None, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.to_tensor(inputs, scale, mean, std, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.to_tensor(inputs, scale, mean, std, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.to_tensor(inputs, scale, mean, std, **kwargs)


@supports()
def to_pil(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.to_pil(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.to_pil(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.to_pil(inputs, **kwargs)


@supports()
def to_numpy(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.to_numpy(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.to_numpy(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.to_numpy(inputs, **kwargs)

#!<-----------------------------------------------------------------------------
#!< FLIP
#!<-----------------------------------------------------------------------------


@supports()
def hflip(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.hflip(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.hflip(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.hflip(inputs, **kwargs)


@supports()
def random_hflip(inputs, p=0.5, **kwargs):
  if random.random() > p:
    return hflip(inputs, **kwargs)
  return inputs


@supports()
def vflip(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.vflip(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.vflip(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.vflip(inputs, **kwargs)


@supports()
def random_vflip(inputs, p=0.5, **kwargs):
  if random.random() > p:
    return vflip(inputs, **kwargs)
  return inputs


@supports()
def flip(inputs, mode, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.flip(inputs, mode=mode, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.flip(inputs, mode=mode, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.flip(inputs, mode=mode, **kwargs)

#!<-----------------------------------------------------------------------------
#!< ROTATE
#!<-----------------------------------------------------------------------------


@supports()
def rotate(inputs, angle, interpolation=T.RESIZE_MODE.BILINEAR, border_mode=T.BORDER_MODE.CONSTANT, border_value=0, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.rotate(inputs, angle=angle, interpolation=interpolation, border_mode=border_mode, border_value=border_value, **kwargs)  # nopep8
  elif isinstance(inputs, Image.Image):
    return F_pil.rotate(inputs, angle=angle, interpolation=interpolation, border_mode=border_mode, border_value=border_value, **kwargs)  # nopep8
  elif isinstance(inputs, torch.Tensor):
    return F_t.rotate(inputs, angle=angle, interpolation=interpolation, border_mode=border_mode, border_value=border_value, **kwargs)  # nopep8


@supports()
def random_rotate(inputs, angle_range=(-30, 30), interpolation=T.RESIZE_MODE.BILINEAR, border_mode=T.BORDER_MODE.CONSTANT, border_value=0, **kwargs):
  angle = random.uniform(angle_range[0], angle_range[1])
  return rotate(inputs, angle=angle, interpolation=interpolation, border_mode=border_mode, border_value=border_value, **kwargs)  # nopep8


#!<-----------------------------------------------------------------------------
#!< AFFINE
#!<-----------------------------------------------------------------------------

@supports()
def affine(inputs, angle: float, tx: float, ty: float, scale: float, shear: float, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.affine(inputs, angle=angle, tx=tx, ty=ty, scale=scale, shear=shear, interpolation=interpolation, **kwargs)  # nopep8
  elif isinstance(inputs, Image.Image):
    return F_pil.affine(inputs, angle=angle, tx=tx, ty=ty, scale=scale, shear=shear, interpolation=interpolation, **kwargs)  # nopep8
  elif isinstance(inputs, torch.Tensor):
    return F_t.affine(inputs, angle=angle, tx=tx, ty=ty, scale=scale, shear=shear, interpolation=interpolation, **kwargs)  # nopep8


@supports()
def affine_theta(inputs, theta, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.affine_theta(inputs, theta=theta, interpolation=interpolation, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.affine_theta(inputs, theta=theta, interpolation=interpolation, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.affine_theta(inputs, theta=theta, interpolation=interpolation, **kwargs)


@supports()
def random_affine(inputs, translates=(0.05, 0.05), zoom=(1.0, 1.5), shear=(0.86, 1.16), rotate=(-10., 10.), preserve_valid=True, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
  theta = F_np._generate_random_affine_theta(translates, zoom, shear, rotate, preserve_valid)
  return affine_theta(inputs, theta, interpolation=interpolation, **kwargs)


#!<-----------------------------------------------------------------------------
#!< COLORSPACE
#!<-----------------------------------------------------------------------------


@supports()
def change_colorspace(inputs, src: T.COLORSPACE, dst: T.COLORSPACE, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.change_colorspace(inputs, src=src, dst=dst, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.change_colorspace(inputs, src=src, dst=dst, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.change_colorspace(inputs, src=src, dst=dst, **kwargs)


@supports()
def to_color(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.to_color(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.to_color(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.to_color(inputs, **kwargs)


@supports()
def to_grayscale(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.to_grayscale(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.to_grayscale(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.to_grayscale(inputs, **kwargs)


@supports()
def rgb_to_yuv709v(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, data_range, 255.0)
  if isinstance(inputs, np.ndarray):
    inputs = F_np.rgb_to_yuv709v(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    inputs = F_pil.rgb_to_yuv709v(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    inputs = F_t.rgb_to_yuv709v(inputs, **kwargs)
  return to_data_range(inputs, 255.0, data_range)


@supports()
def rgb_to_yuv709f(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, data_range, 255.0)
  if isinstance(inputs, np.ndarray):
    inputs = F_np.rgb_to_yuv709f(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    inputs = F_pil.rgb_to_yuv709f(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    inputs = F_t.rgb_to_yuv709f(inputs, **kwargs)
  return to_data_range(inputs, 255.0, data_range)


@supports()
def yuv709v_to_rgb(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, data_range, 255.0)
  if isinstance(inputs, np.ndarray):
    inputs = F_np.yuv709v_to_rgb(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    inputs = F_pil.yuv709v_to_rgb(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    inputs = F_t.yuv709v_to_rgb(inputs, **kwargs)
  return to_data_range(inputs, 255.0, data_range)


@supports()
def yuv709f_to_rgb(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, data_range, 255.0)
  if isinstance(inputs, np.ndarray):
    inputs = F_np.yuv709f_to_rgb(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    inputs = F_pil.yuv709f_to_rgb(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    inputs = F_t.yuv709f_to_rgb(inputs, **kwargs)
  return to_data_range(inputs, 255.0, data_range)


@supports()
def rgb_to_bgr(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, data_range, 255.0)
  if isinstance(inputs, np.ndarray):
    inputs = F_np.rgb_to_bgr(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    inputs = F_pil.rgb_to_bgr(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    inputs = F_t.rgb_to_bgr(inputs, **kwargs)
  return to_data_range(inputs, 255.0, data_range)


@supports()
def bgr_to_rgb(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, data_range, 255.0)
  if isinstance(inputs, np.ndarray):
    inputs = F_np.bgr_to_rgb(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    inputs = F_pil.bgr_to_rgb(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    inputs = F_t.bgr_to_rgb(inputs, **kwargs)
  return to_data_range(inputs, 255.0, data_range)


@supports()
def rgb_to_yuv601(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, data_range, 1.0)
  if isinstance(inputs, np.ndarray):
    inputs = F_np.rgb_to_yuv601(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    inputs = F_pil.rgb_to_yuv601(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    inputs = F_t.rgb_to_yuv601(inputs, **kwargs)
  return to_data_range(inputs, 255.0, data_range)


@supports()
def yuv601_to_rgb(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, data_range, 1.0)
  if isinstance(inputs, np.ndarray):
    inputs = F_np.yuv601_to_rgb(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    inputs = F_pil.yuv601_to_rgb(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    inputs = F_t.yuv601_to_rgb(inputs, **kwargs)
  return to_data_range(inputs, 255.0, data_range)


@supports()
def rgb_to_yiq(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, data_range, 255.0)
  if isinstance(inputs, np.ndarray):
    inputs = F_np.rgb_to_yiq(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    inputs = F_pil.rgb_to_yiq(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    inputs = F_t.rgb_to_yiq(inputs, **kwargs)
  return to_data_range(inputs, 255.0, data_range)


@supports()
def rgb_to_lhm(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, data_range, 255.0)
  if isinstance(inputs, np.ndarray):
    inputs = F_np.rgb_to_lhm(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    inputs = F_pil.rgb_to_lhm(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    inputs = F_t.rgb_to_lhm(inputs, **kwargs)
  return to_data_range(inputs, 255.0, data_range)


@supports()
def rgb_to_xyz(inputs, data_range=255.0, **kwargs):
  inputs = to_data_range(inputs, data_range, 1.0)
  if isinstance(inputs, np.ndarray):
    inputs = F_np.rgb_to_xyz(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    inputs = F_pil.rgb_to_xyz(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    inputs = F_t.rgb_to_xyz(inputs, **kwargs)
  return inputs


@supports()
def xyz_to_lab(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    inputs = F_np.xyz_to_lab(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    inputs = F_pil.xyz_to_lab(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    inputs = F_t.xyz_to_lab(inputs, **kwargs)
  return inputs


@supports()
def rgb_to_lab(inputs, data_range=255.0, **kwargs):
  return xyz_to_lab(rgb_to_xyz(inputs, data_range=data_range, **kwargs), **kwargs)

#!<-----------------------------------------------------------------------------
#!< PHOTOMETRIC
#!<-----------------------------------------------------------------------------


@supports()
def adjust_sharpness(inputs, factor, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.adjust_sharpness(inputs, factor=factor, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.adjust_sharpness(inputs, factor=factor, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.adjust_sharpness(inputs, factor=factor, **kwargs)


@supports()
def adjust_brightness(inputs, factor, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.adjust_brightness(inputs, factor=factor, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.adjust_brightness(inputs, factor=factor, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.adjust_brightness(inputs, factor=factor, **kwargs)


@supports()
def adjust_contrast(inputs, factor, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.adjust_contrast(inputs, factor=factor, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.adjust_contrast(inputs, factor=factor, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.adjust_contrast(inputs, factor=factor, **kwargs)


@supports()
def adjust_gamma(inputs, factor, gain, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.adjust_gamma(inputs, factor=factor, gain=gain, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.adjust_gamma(inputs, factor=factor, gain=gain, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.adjust_gamma(inputs, factor=factor, gain=gain, **kwargs)


@supports()
def adjust_hue(inputs, factor, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.adjust_hue(inputs, factor=factor, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.adjust_hue(inputs, factor=factor, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.adjust_hue(inputs, factor=factor, **kwargs)


@supports()
def adjust_saturation(inputs, factor, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.adjust_saturation(inputs, factor=factor, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.adjust_saturation(inputs, factor=factor, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.adjust_saturation(inputs, factor=factor, **kwargs)


@supports()
def adjust_saturation(inputs, factor, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.adjust_saturation(inputs, factor=factor, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.adjust_saturation(inputs, factor=factor, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.adjust_saturation(inputs, factor=factor, **kwargs)


@supports()
def photometric_distortion(inputs,
                           brightness_delta=32,
                           contrast_range=(0.5, 1.5),
                           saturation_range=(0.5, 1.5),
                           hue_delta=18,
                           **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.photometric_distortion(
        inputs,
        brightness_delta=brightness_delta,
        contrast_range=contrast_range,
        saturation_range=saturation_range,
        hue_delta=hue_delta,
        **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.photometric_distortion(
        inputs,
        brightness_delta=brightness_delta,
        contrast_range=contrast_range,
        saturation_range=saturation_range,
        hue_delta=hue_delta,
        **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.photometric_distortion(
        inputs,
        brightness_delta=brightness_delta,
        contrast_range=contrast_range,
        saturation_range=saturation_range,
        hue_delta=hue_delta,
        **kwargs)


#!<-----------------------------------------------------------------------------
#!< CROP AND PADDING
#!<-----------------------------------------------------------------------------


@supports()
def crop(inputs, top, left, height, width, **kwargs):
  """Crop the given image at specified location and output size.
  If the image is torch Tensor, it is expected to have [..., H, W] shape, where ... means an arbitrary number of leading dimensions.
  If image size is smaller than output size along any edge, image is padded with 0 and then cropped.

  Args:
      inputs: Image to be cropped. (0,0) denotes the top left corner of the image.
      top (int): Vertical component of the top left corner of the crop box.
      left (int): Horizontal component of the top left corner of the crop box.
      height (int): Height of the crop box.
      width (int): Width of the crop box.

  """
  if isinstance(inputs, np.ndarray):
    return F_np.crop(inputs, top, left, height, width, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.crop(inputs, top, left, height, width, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.crop(inputs, top, left, height, width,  **kwargs)


@supports()
def pad(inputs, left, top, right, bottom, fill_value=0, mode='constant', **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.pad(inputs, left=left, top=top, right=right, bottom=bottom, fill_value=fill_value, mode=mode, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.pad(inputs, left=left, top=top, right=right, bottom=bottom, fill_value=fill_value, mode=mode, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.pad(inputs, left=left, top=top, right=right, bottom=bottom, fill_value=fill_value, mode=mode, **kwargs)


@supports()
def crop_and_pad(inputs,
                 src_crop_y,
                 src_crop_x,
                 src_crop_h,
                 src_crop_w,
                 dst_crop_x,
                 dst_crop_y,
                 dst_height,
                 dst_width,
                 fill_value=0,
                 mode='constant',
                 **kwargs):
  """crop an area from source image and paste to dst
  """
  if isinstance(inputs, np.ndarray):
    return F_np.crop_and_pad(
        inputs,
        src_crop_y=src_crop_y,
        src_crop_x=src_crop_x,
        src_crop_h=src_crop_h,
        src_crop_w=src_crop_w,
        dst_crop_x=dst_crop_x,
        dst_crop_y=dst_crop_y,
        dst_height=dst_height,
        dst_width=dst_width,
        fill_value=fill_value,
        mode=mode,
        **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.crop_and_pad(
        inputs,
        src_crop_y=src_crop_y,
        src_crop_x=src_crop_x,
        src_crop_h=src_crop_h,
        src_crop_w=src_crop_w,
        dst_crop_x=dst_crop_x,
        dst_crop_y=dst_crop_y,
        dst_height=dst_height,
        dst_width=dst_width,
        fill_value=fill_value,
        mode=mode,
        **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.crop_and_pad(
        inputs,
        src_crop_y=src_crop_y,
        src_crop_x=src_crop_x,
        src_crop_h=src_crop_h,
        src_crop_w=src_crop_w,
        dst_crop_x=dst_crop_x,
        dst_crop_y=dst_crop_y,
        dst_height=dst_height,
        dst_width=dst_width,
        fill_value=fill_value,
        mode=mode,
        **kwargs)


@supports()
def random_crop(inputs, height, width, **kwargs):
  """random crop, require width and height less than image

  Args:
      height (int or float): output height, or keep ratio (0 ~ 1)
      width (int or float): output width, or keep ratio (0 ~ 1)

  """
  def _get_coords(img_h, img_w, crop_h, crop_w, rh, rw):
    y1 = int((img_h - crop_h) * rh)
    y2 = y1 + crop_h
    x1 = int((img_w - crop_w) * rw)
    x2 = x1 + crop_w
    return x1, y1, x2, y2

  h, w = get_inputs_hw(inputs)
  rh = random.random()
  rw = random.random()

  new_width = int(w * width) if width < 1 else width
  new_height = int(h * height) if height < 1 else height
  x1, y1, x2, y2 = _get_coords(h, w, new_height, new_width, rh, rw)

  return crop(inputs, y1, x1, y2 - y1, x2 - x1, **kwargs)


@supports()
def center_crop(inputs, height, width, **kwargs):
  """crop inputs to target height and width.

  Args:
      height (int or float): output height
      width (int or float): output width

  """
  def _get_coords(height, width, crop_height, crop_width):
    y1 = (height - crop_height) // 2
    y2 = y1 + crop_height
    x1 = (width - crop_width) // 2
    x2 = x1 + crop_width
    return x1, y1, x2, y2

  h, w = get_inputs_hw(inputs)
  x1, y1, x2, y2 = _get_coords(h, w, height, width)

  return crop(inputs, y1, x1, y2 - y1 + 1, x2 - x1 + 1, **kwargs)


@supports()
def center_crop_and_pad(inputs, height, width, fill_value=0, **kwargs):
  """center crop and padding image to target_height and target_width

    if image width or height is smaller than target size, it will prefer to pad
      to max side and then implement center crop.

    if image width or height is less than target size, it will center paste image
      to target size.

  Args:
      height ([int]): target height
      width ([int]): target width
      fill_value ([float]): default to 0
  """
  h, w = get_inputs_hw(inputs)
  crop_x = max([0, (w - width) // 2])
  crop_y = max([0, (h - height) // 2])
  crop_h = min([height, h])
  crop_w = min([width, w])
  dst_y = max([0, (height - h) // 2])
  dst_x = max([0, (width - w) // 2])
  return crop_and_pad(
      inputs,
      src_crop_y=crop_y,
      src_crop_x=crop_x,
      src_crop_h=crop_h,
      src_crop_w=crop_w,
      dst_crop_y=dst_y,
      dst_crop_x=dst_x,
      dst_height=height,
      dst_width=width,
      fill_value=fill_value,
      mode='constant')


@supports()
def resized_crop(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.resized_crop(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.resized_crop(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.resized_crop(inputs, **kwargs)


@supports()
def ten_crop(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.ten_crop(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.ten_crop(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.ten_crop(inputs, **kwargs)


@supports()
def five_crop(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.five_crop(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.five_crop(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.five_crop(inputs, **kwargs)


@supports()
def non_overlap_crop_patch(inputs, patch_size=32, stride=32, **kwargs):
  """non-overlapp crop.

    For a image [H, W, C], it will be divided into [N, patch_size, patch_size, C]
      N = ((h + patch_size) // (patch_size * stride)) * ((w + patch_size) // (patch_size * stride))

  Args:
      patch_size (int, optional): Defaults to 32.
      stride (int, optional): Defaults to 32.

  """
  if isinstance(inputs, np.ndarray):
    return F_np.non_overlap_crop_patch(inputs, patch_size=patch_size, stride=stride, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.non_overlap_crop_patch(inputs, patch_size=patch_size, stride=stride, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.non_overlap_crop_patch(inputs, patch_size=patch_size, stride=stride, **kwargs)


@supports()
def pad_to_size_divisible(inputs, size_divisible=32, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.pad_to_size_divisible(inputs, size_divisible=size_divisible, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.pad_to_size_divisible(inputs, size_divisible=size_divisible, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.pad_to_size_divisible(inputs, size_divisible=size_divisible, **kwargs)


@supports()
def pad_to_square(inputs, fill_value=0, **kwargs):
  """pad input to square (old image located on left top of new image.)

  Args:
      fill_value (int, optional): [description]. Defaults to 0.

  """
  h, w = get_inputs_hw(inputs)
  long_side = max(w, h)
  w_pad = w - long_side
  h_pad = h - long_side
  return pad(inputs, left=0, right=w_pad, top=0, bottom=h_pad, fill_value=fill_value, **kwargs)


@supports()
def pad_to_target_size(inputs, height, width, fill_value=0, **kwargs):
  h, w = get_inputs_hw(inputs)
  assert height >= h and width >= w
  h_pad = height - h
  w_pad = width - w
  return pad(inputs, left=0, right=w_pad, top=0, bottom=h_pad, fill_value=fill_value, **kwargs)


#!<-----------------------------------------------------------------------------
#!< RESIZE
#!<-----------------------------------------------------------------------------


@supports()
def resize(inputs, height, width, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
  """resize to given size

  Args:
      height (int): _description_
      width (int): _description_
      interpolation (_type_, optional): _description_. Defaults to T.RESIZE_MODE.BILINEAR.

  """
  if isinstance(inputs, np.ndarray):
    return F_np.resize(inputs, height=height, width=width, interpolation=interpolation, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.resize(inputs, height=height, width=width, interpolation=interpolation, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.resize(inputs, height=height, width=width, interpolation=interpolation, **kwargs)


@supports()
def random_resize(inputs, scale_range=(1, 4), interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
  """random resize inputs with aspect ratio.

  Args:
      scale_range (tuple, optional): [description]. Defaults to (1, 4).
      interpolation ([type], optional): [description]. Defaults to cv2.INTER_LINEAR.

  """
  _min, _max = scale_range
  scale = random.random() * (_max - _min) + _min
  h, w = get_inputs_hw(inputs)
  return resize(inputs, int(h * scale), int(w * scale), interpolation=interpolation, **kwargs)


@supports()
def shortside_resize(inputs, min_size=256, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
  """inputs will be aspect sized by short side to min_size.

  Args:
      inputs ([type]): [description]
      min_size (int): image will aspect resize according to short side size.
      interpolation ([type], optional): [description]. Defaults to cv2.INTER_LINEAR.

  Returns:
      [type]: [description]
  """
  def _get_shortside_shape(h, w, min_size):
    if (w <= h and w == min_size) or (h <= w and h == min_size):
      ow, oh = w, h
    # resize
    if w < h:
      ow = min_size
      oh = int(min_size * h / w)
    else:
      oh = min_size
      ow = int(min_size * w / h)
    return oh, ow

  h, w = get_inputs_hw(inputs)
  oh, ow = _get_shortside_shape(h, w, min_size)

  return resize(inputs, height=oh, width=ow, interpolation=interpolation, **kwargs)


@supports()
def adaptive_resize(inputs, height, width, interpolation=T.RESIZE_MODE.BILINEAR, **kwargs):
  """resize image make it less than target height and width
  """
  h, w = get_inputs_hw(inputs)
  if h < height or w < width:
    return inputs
  return shortside_resize(inputs, min_size=min(height, width), interpolation=interpolation, **kwargs)


#!<-----------------------------------------------------------------------------
#!< FILTER
#!<-----------------------------------------------------------------------------


@supports()
def iso_noise(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.default(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.default(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.default(inputs, **kwargs)


@supports()
def gaussian_noise(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.default(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.default(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.default(inputs, **kwargs)


@supports()
def gaussian_blur(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.default(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.default(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.default(inputs, **kwargs)


@supports()
def motion_blur(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.default(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.default(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.default(inputs, **kwargs)


@supports()
def median_blur(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.default(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.default(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.default(inputs, **kwargs)


@supports()
def sobel(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.default(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.default(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.default(inputs, **kwargs)

#!<-----------------------------------------------------------------------------
#!< MORPHOLOGY
#!<-----------------------------------------------------------------------------


@supports()
def alpha_to_trimap(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.default(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.default(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.default(inputs, **kwargs)

#!<-----------------------------------------------------------------------------
#!< NORMALIZE
#!<-----------------------------------------------------------------------------


@supports()
def equal_hist(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.default(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.default(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.default(inputs, **kwargs)


@supports()
def truncated_standardize(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.default(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.default(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.default(inputs, **kwargs)


@supports()
def local_contrast_normalize(inputs, **kwargs):
  if isinstance(inputs, np.ndarray):
    return F_np.default(inputs, **kwargs)
  elif isinstance(inputs, Image.Image):
    return F_pil.default(inputs, **kwargs)
  elif isinstance(inputs, torch.Tensor):
    return F_t.default(inputs, **kwargs)
