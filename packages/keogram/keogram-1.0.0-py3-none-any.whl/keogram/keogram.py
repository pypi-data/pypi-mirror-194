#  MIT License
#
#  Copyright (c) 2023 Night Works
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
import dataclasses
import json
import logging
import os
from dataclasses import dataclass
from typing import Union

from PIL import Image

logger = logging.getLogger(__name__)


@dataclass
class MetaData:
    source: str
    destination: str
    file_name: str
    final_path: str
    height: int
    width: int
    valid_image: int
    invalid_files: [str]


def create(source: Union[str, os.PathLike], destination: Union[str, os.PathLike],
           keogram_file: str = "keogram.jpg", metadata: bool = False) -> MetaData:
    """
    Creates a Keogram from all the image files found in the source directory and saves the resulting image in
    destination/keogram_file. Checks the existence of the source directory and creates the destination directory if
    it already doesn't exist.

    Args:
        source: location of the images to be processed
        destination: destination directory to save the resulting keogram
        keogram_file: file name for the resulting image defaults to keogram.jpg if setting a custom name be sure to
                      include the file type extension
        metadata: generates a json file of metadata of data used to create keogram

    Returns:
        the metadata for the created keogram with information for further processing

    Raises:
        NotADirectoryError: if the source is a file or the directory can not be found
    """
    if os.path.exists(source):
        logger.debug('%s exists on the file system', source)
        if os.path.isfile(source):
            logger.error('%s is not a directory', source)
            raise NotADirectoryError('%s is not a directory', source)
        else:
            if not os.path.exists(destination):
                logger.debug('%s does not exist, creating directories', destination)
                os.makedirs(destination)
            logger.debug('source and destination directories exist beginning to process images')
            return _process_images(source, destination, keogram_file, metadata)
    else:
        logger.error('%s does not exist', source)
        raise NotADirectoryError('%s does not exist', source)


def _save_metadata(metadata: MetaData) -> None:
    """
    Saves the metadata from the creation of the keogram to the file system alongside the keogram
    Args:
        metadata: The MetaData object to be converted to json and saved
    """
    json_file_name = os.path.splitext(metadata.file_name)[0]
    json_data = json.dumps(dataclasses.asdict(metadata), indent=4)
    with open(f"{metadata.destination}/{json_file_name}.json", "w") as outfile:
        outfile.write(json_data)


def _process_images(source: Union[str, os.PathLike], destination: Union[str, os.PathLike], file_name: str,
                    metadata: bool = False) -> MetaData:
    """
    Creates a Keogram from all the image files found in the source directory and saves the resulting image in
    destination/keogram_file. No checks are performed on the source and destination directories.

    Args:
        source: The directory that contains the images to be processed into a keogram
        destination: The output directory to save the completed keogram image
        file_name: The filename to be used for the resulting keogram image including the file extension
        metadata: Save the keogram metadata alongside the resulting image as json

    Returns:
        the metadata for the created keogram with information for further processing
    """
    keogram_image = Image.new("RGB", (0, 0))

    sorted_files = sorted(os.listdir(source))
    logger.debug(f"source directory contains {len(sorted_files)} files")

    invalid = []

    for file_item in sorted_files:
        if not valid_image(file_item):
            logger.warning(f"{file_item} is not a valid image type")
            invalid.append(file_item)
            continue
        current_image = Image.open(os.path.join(source, file_item))
        image_middle = int(current_image.width / 2)
        center_slice = (image_middle, 0, image_middle + 1, current_image.height)
        current_image = current_image.crop(center_slice)
        keogram_image = concat_images(keogram_image, current_image)

    file_destination = f"{destination}/{file_name}"
    keogram_image.save(file_destination)

    keogram_image_metadata = MetaData(source=source, destination=destination, file_name=file_name,
                                      final_path=file_destination, width=keogram_image.width,
                                      height=keogram_image.height,
                                      invalid_files=invalid, valid_image=len(sorted_files) - len(invalid))
    if metadata:
        _save_metadata(keogram_image_metadata)

    return keogram_image_metadata


def valid_image(file: Union[str, os.PathLike]) -> bool:
    """
    Takes a file and checks to see if it's a supported source file type.

    Args:
        file: The file to be checked for a correct extension type

    Returns: True if the file is supported otherwise False

    """
    valid_images = [".jpg", ".gif", ".png", ".jpeg"]
    file_extension = os.path.splitext(file)[1]
    logger.debug(f"checking image type of {file} with extension of {file_extension}")
    return file_extension.lower() in valid_images


def concat_images(left_image: Image, right_image: Image) -> Image:
    """
    Takes two images and joins them together, the right image is appended to the left image resulting in a new image
    this image will always be the height of the second image that's passed.

    Args:
        left_image: The image to be on the left of the resulting image
        right_image: The image to be joined to the right of the resulting image

    Returns: The final image of the two being joined together

    """
    logger.debug("concatenating base image with new image slice")
    logger.debug(f"base image size {left_image.width} x {left_image.height}")
    new_image = Image.new('RGB', (left_image.width + right_image.width, right_image.height))
    new_image.paste(left_image, (0, 0))
    new_image.paste(right_image, (left_image.width, 0))
    logger.debug(f"new image size {new_image.width} x {new_image.height}")
    return new_image
