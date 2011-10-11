#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#

"""Image manipulation API.

Classes defined in this module:
  Image: class used to encapsulate image information and transformations for
    that image.

    The current manipulations that are available are resize, rotate,
    horizontal_flip, vertical_flip, crop and im_feeling_lucky.

    It should be noted that each transform can only be called once per image
    per execute_transforms() call.
"""



from google.appengine.api import apiproxy_stub_map
from google.appengine.api.images import images_service_pb
from google.appengine.runtime import apiproxy_errors


JPEG = images_service_pb.OutputSettings.JPEG
PNG = images_service_pb.OutputSettings.PNG

OUTPUT_ENCODING_TYPES = frozenset([JPEG, PNG])


class Error(Exception):
  """Base error class for this module."""


class TransformationError(Error):
  """Error while attempting to transform the image."""


class BadRequestError(Error):
  """The parameters given had something wrong with them."""


class NotImageError(Error):
  """The image data given is not recognizable as an image."""


class BadImageError(Error):
  """The image data given is corrupt."""


class LargeImageError(Error):
  """The image data given is too large to process."""


class Image(object):
  """Image object to manipulate."""

  def __init__(self, image_data):
    """Constructor.

    Args:
      image_data: str, image data in string form.

    Raises:
      NotImageError if the given data is empty.
    """
    if not image_data:
      raise NotImageError("Empty image data.")

    self._image_data = image_data
    self._transforms = []
    self._transform_map = {}

  def _check_transform_limits(self, transform):
    """Ensure some simple limits on the number of transforms allowed.

    Args:
      transform: images_service_pb.ImagesServiceTransform, enum of the
        trasnform called.

    Raises:
      BadRequestError if the transform has already been requested for the image.
    """
    if not images_service_pb.ImagesServiceTransform.Type_Name(transform):
      raise BadRequestError("'%s' is not a valid transform." % transform)

    if transform in self._transform_map:
      transform_name = images_service_pb.ImagesServiceTransform.Type_Name(
          transform)
      raise BadRequestError("A '%s' transform has already been "
                            "requested on this image." % transform_name)
    self._transform_map[transform] = True

  def resize(self, width=0, height=0):
    """Resize the image maintaining the aspect ratio.

    If both width and height are specified, the more restricting of the two
    values will be used when resizing the photo.  The maximum dimension allowed
    for both width and height is 4000 pixels.

    Args:
      width: int, width (in pixels) to change the image width to.
      height: int, height (in pixels) to change the image height to.

    Raises:
      TypeError when width or height is not either 'int' or 'long' types.
      BadRequestError when there is something wrong with the given height or
        width or if a Resize has already been requested on this image.
    """
    if (not isinstance(width, (int, long)) or
        not isinstance(height, (int, long))):
      raise TypeError("Width and height must be integers.")
    if width < 0 or height < 0:
      raise BadRequestError("Width and height must be >= 0.")

    if not width and not height:
      raise BadRequestError("At least one of width or height must be > 0.")

    if width > 4000 or height > 4000:
      raise BadRequestError("Both width and height must be < 4000.")

    self._check_transform_limits(
        images_service_pb.ImagesServiceTransform.RESIZE)

    transform = images_service_pb.Transform()
    transform.set_width(width)
    transform.set_height(height)

    self._transforms.append(transform)

  def rotate(self, degrees):
    """Rotate an image a given number of degrees clockwise.

    Args:
      degrees: int, must be a multiple of 90.

    Raises:
      TypeError when degrees is not either 'int' or 'long' types.
      BadRequestError when there is something wrong with the given degrees or
      if a Rotate trasnform has already been requested.
    """
    if not isinstance(degrees, (int, long)):
      raise TypeError("Degrees must be integers.")

    if degrees % 90 != 0:
      raise BadRequestError("degrees argument must be multiple of 90.")

    degrees = degrees % 360

    self._check_transform_limits(
        images_service_pb.ImagesServiceTransform.ROTATE)

    transform = images_service_pb.Transform()
    transform.set_rotate(degrees)

    self._transforms.append(transform)

  def horizontal_flip(self):
    """Flip the image horizontally.

    Raises:
      BadRequestError if a HorizontalFlip has already been requested on the
      image.
    """
    self._check_transform_limits(
        images_service_pb.ImagesServiceTransform.HORIZONTAL_FLIP)

    transform = images_service_pb.Transform()
    transform.set_horizontal_flip(True)

    self._transforms.append(transform)

  def vertical_flip(self):
    """Flip the image vertically.

    Raises:
      BadRequestError if a HorizontalFlip has already been requested on the
      image.
    """
    self._check_transform_limits(
        images_service_pb.ImagesServiceTransform.VERTICAL_FLIP)
    transform = images_service_pb.Transform()
    transform.set_vertical_flip(True)

    self._transforms.append(transform)

  def _validate_crop_arg(self, val, val_name):
    """Validate the given value of a Crop() method argument.

    Args:
      val: float, value of the argument.
      val_name: str, name of the argument.

    Raises:
      TypeError if the args are not of type 'float'.
      BadRequestError when there is something wrong with the given bounding box.
    """
    if type(val) != float:
      raise TypeError("arg '%s' must be of type 'float'." % val_name)

    if not (0 <= val <= 1.0):
      raise BadRequestError("arg '%s' must be between 0.0 and 1.0 "
                            "(inclusive)" % val_name)

  def crop(self, left_x, top_y, right_x, bottom_y):
    """Crop the image.

    The four arguments are the scaling numbers to describe the bounding box
    which will crop the image.  The upper left point of the bounding box will
    be at (left_x*image_width, top_y*image_height) the lower right point will
    be at (right_x*image_width, bottom_y*image_height).

    Args:
      left_x: float value between 0.0 and 1.0 (inclusive).
      top_y: float value between 0.0 and 1.0 (inclusive).
      right_x: float value between 0.0 and 1.0 (inclusive).
      bottom_y: float value between 0.0 and 1.0 (inclusive).

    Raises:
      TypeError if the args are not of type 'float'.
      BadRequestError when there is something wrong with the given bounding box
        or if there has already been a crop transform requested for this image.
    """
    self._validate_crop_arg(left_x, "left_x")
    self._validate_crop_arg(top_y, "top_y")
    self._validate_crop_arg(right_x, "right_x")
    self._validate_crop_arg(bottom_y, "bottom_y")

    if left_x >= right_x:
      raise BadRequestError("left_x must be less than right_x")
    if top_y >= bottom_y:
      raise BadRequestError("top_y must be less than bottom_y")

    self._check_transform_limits(images_service_pb.ImagesServiceTransform.CROP)

    transform = images_service_pb.Transform()
    transform.set_crop_left_x(left_x)
    transform.set_crop_top_y(top_y)
    transform.set_crop_right_x(right_x)
    transform.set_crop_bottom_y(bottom_y)

    self._transforms.append(transform)

  def im_feeling_lucky(self):
    """Automatically adjust image contrast and color levels.

    This is similar to the "I'm Feeling Lucky" button in Picasa.

    Raises:
      BadRequestError if this transform has already been requested for this
      image.
    """
    self._check_transform_limits(
        images_service_pb.ImagesServiceTransform.IM_FEELING_LUCKY)
    transform = images_service_pb.Transform()
    transform.set_autolevels(True)

    self._transforms.append(transform)

  def execute_transforms(self, output_encoding=PNG):
    """Perform transformations on given image.

    Args:
      output_encoding: A value from OUTPUT_ENCODING_TYPES.

    Returns:
      str, image data after the transformations have been performed on it.

    Raises:
      BadRequestError when there is something wrong with the request
        specifications.
      NotImageError when the image data given is not an image.
      BadImageError when the image data given is corrupt.
      LargeImageError when the image data given is too large to process.
      TransformtionError when something errors during image manipulation.
      Error when something unknown, but bad, happens.
    """
    if output_encoding not in OUTPUT_ENCODING_TYPES:
      raise BadRequestError("Output encoding type not in recognized set "
                            "%s" % OUTPUT_ENCODING_TYPES)

    if not self._transforms:
      raise BadRequestError("Must specify at least one transformation.")

    request = images_service_pb.ImagesTransformRequest()
    response = images_service_pb.ImagesTransformResponse()

    request.mutable_image().set_content(self._image_data)

    for transform in self._transforms:
      request.add_transform().CopyFrom(transform)

    request.mutable_output().set_mime_type(output_encoding)

    try:
      apiproxy_stub_map.MakeSyncCall("images",
                                     "Transform",
                                     request,
                                     response)
    except apiproxy_errors.ApplicationError, e:
      if (e.application_error ==
          images_service_pb.ImagesServiceError.BAD_TRANSFORM_DATA):
        raise BadRequestError()
      elif (e.application_error ==
            images_service_pb.ImagesServiceError.NOT_IMAGE):
        raise NotImageError()
      elif (e.application_error ==
            images_service_pb.ImagesServiceError.BAD_IMAGE_DATA):
        raise BadImageError()
      elif (e.application_error ==
            images_service_pb.ImagesServiceError.IMAGE_TOO_LARGE):
        raise LargeImageError()
      elif (e.application_error ==
            images_service_pb.ImagesServiceError.UNSPECIFIED_ERROR):
        raise TransformationError()
      else:
        raise Error()

    self._image_data = response.image().content()
    self._transforms = []
    self._transform_map.clear()
    return self._image_data


def resize(image_data, width=0, height=0, output_encoding=PNG):
  """Resize a given image file maintaining the aspect ratio.

  If both width and height are specified, the more restricting of the two
  values will be used when resizing the photo.  The maximum dimension allowed
  for both width and height is 4000 pixels.

  Args:
    image_data: str, source image data.
    width: int, width (in pixels) to change the image width to.
    height: int, height (in pixels) to change the image height to.
    output_encoding: a value from OUTPUT_ENCODING_TYPES.

  Raises:
    TypeError when width or height not either 'int' or 'long' types.
    BadRequestError when there is something wrong with the given height or
      width or if a Resize has already been requested on this image.
    Error when something went wrong with the call.  See Image.ExecuteTransforms
      for more details.
  """
  image = Image(image_data)
  image.resize(width, height)
  return image.execute_transforms(output_encoding=output_encoding)


def rotate(image_data, degrees, output_encoding=PNG):
  """Rotate a given image a given number of degrees clockwise.

  Args:
    image_data: str, source image data.
    degrees: value from ROTATE_DEGREE_VALUES.
    output_encoding: a value from OUTPUT_ENCODING_TYPES.

  Raises:
    TypeError when degrees is not either 'int' or 'long' types.
    BadRequestError when there is something wrong with the given degrees or
    if a Rotate trasnform has already been requested.
    Error when something went wrong with the call.  See Image.ExecuteTransforms
      for more details.
  """
  image = Image(image_data)
  image.rotate(degrees)
  return image.execute_transforms(output_encoding=output_encoding)


def horizontal_flip(image_data, output_encoding=PNG):
  """Flip the image horizontally.

  Args:
    image_data: str, source image data.
    output_encoding: a value from OUTPUT_ENCODING_TYPES.

  Raises:
    Error when something went wrong with the call.  See Image.ExecuteTransforms
      for more details.
  """
  image = Image(image_data)
  image.horizontal_flip()
  return image.execute_transforms(output_encoding=output_encoding)


def vertical_flip(image_data, output_encoding=PNG):
  """Flip the image vertically.

  Args:
    image_data: str, source image data.
    output_encoding: a value from OUTPUT_ENCODING_TYPES.

  Raises:
    Error when something went wrong with the call.  See Image.ExecuteTransforms
      for more details.
  """
  image = Image(image_data)
  image.vertical_flip()
  return image.execute_transforms(output_encoding=output_encoding)


def crop(image_data, left_x, top_y, right_x, bottom_y, output_encoding=PNG):
  """Crop the given image.

  The four arguments are the scaling numbers to describe the bounding box
  which will crop the image.  The upper left point of the bounding box will
  be at (left_x*image_width, top_y*image_height) the lower right point will
  be at (right_x*image_width, bottom_y*image_height).

  Args:
    image_data: str, source image data.
    left_x: float value between 0.0 and 1.0 (inclusive).
    top_y: float value between 0.0 and 1.0 (inclusive).
    right_x: float value between 0.0 and 1.0 (inclusive).
    bottom_y: float value between 0.0 and 1.0 (inclusive).
    output_encoding: a value from OUTPUT_ENCODING_TYPES.

  Raises:
    TypeError if the args are not of type 'float'.
    BadRequestError when there is something wrong with the given bounding box
      or if there has already been a crop transform requested for this image.
    Error when something went wrong with the call.  See Image.ExecuteTransforms
      for more details.
  """
  image = Image(image_data)
  image.crop(left_x, top_y, right_x, bottom_y)
  return image.execute_transforms(output_encoding=output_encoding)


def im_feeling_lucky(image_data, output_encoding=PNG):
  """Automatically adjust image levels.

  This is similar to the "I'm Feeling Lucky" button in Picasa.

  Args:
    image_data: str, source image data.
    output_encoding: a value from OUTPUT_ENCODING_TYPES.

  Raises:
    Error when something went wrong with the call.  See Image.ExecuteTransforms
      for more details.
  """
  image = Image(image_data)
  image.im_feeling_lucky()
  return image.execute_transforms(output_encoding=output_encoding)
