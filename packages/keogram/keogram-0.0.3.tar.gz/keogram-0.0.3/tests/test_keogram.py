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

import os
import shutil
from unittest.mock import patch

import pytest
from PIL import Image

from src.keogram.keogram import valid_image, concat_images, create

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize("valid_format", ["jpg", "gif", "png", "jpeg", "JPG", "GIF", "PNG", "JPEG"])
def test_valid_image_formats(valid_format):
    assert valid_image(f"/something/test.{valid_format}")


@pytest.mark.parametrize("invalid_format", ["tif", "dng", "raw", "pdf", "tiff", "TIF", "DNG", "RAW", "TIFF"])
def test_invalid_image_formats(invalid_format):
    assert not valid_image(f"/something/test.{invalid_format}")


def test_concat_images():
    first = Image.new("RGB", (10, 10))
    second = Image.new("RGB", (15, 10))
    result = concat_images(first, second)
    assert result.width == 25
    assert result.height == 10


def test_concat_second_image_taller():
    first = Image.new("RGB", (10, 10))
    second = Image.new("RGB", (15, 30))
    result = concat_images(first, second)
    assert result.width == 25
    assert result.height == 30


def test_concat_first_image_taller():
    first = Image.new("RGB", (10, 50))
    second = Image.new("RGB", (15, 30))
    result = concat_images(first, second)
    assert result.width == 25
    assert result.height == 30


def test_source_not_file():
    with pytest.raises(NotADirectoryError):
        create(f"{ROOT_DIR}/test_keogram.py", "")


def test_source_directory_not_exist():
    with pytest.raises(NotADirectoryError):
        create(f"{ROOT_DIR}/not_found/", "")


@patch("src.keogram.keogram._process_images")
@patch("src.keogram.keogram.os.makedirs")
def test_output_directories_created(mock_makedir, mock_process):
    create(ROOT_DIR, f"{ROOT_DIR}/created")
    mock_makedir.assert_called_with(f"{ROOT_DIR}/created")
    mock_process.assert_called()


def test_create_keogram():
    output_folder = f"{ROOT_DIR}/output"
    shutil.rmtree(output_folder, ignore_errors=True)
    file_name = "test_image.jpg"
    assert not os.path.exists(f"{output_folder}/{file_name}")
    create(f"{ROOT_DIR}/test_image", output_folder, file_name, True)
    assert os.path.exists(f"{output_folder}/{file_name}")
