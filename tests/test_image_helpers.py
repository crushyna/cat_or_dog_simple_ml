import pytest

from PIL import Image
from helpers.image_helpers import ImageHelpers
from helpers.string_helpers import StringHelpers


class TestImageHelpers:
    def test_create_thumbnail(self):
        test_filename = 'cat_example.jpg'
        test_filename_thumbnail = f"static/resources/temp/cat_example_thumbnail.jpg"
        ImageHelpers.create_thumbnail(test_filename, test_filename_thumbnail)
        test_image = Image.open(test_filename_thumbnail)
        assert test_image.size[0] <= 400
        assert test_image.size[1] <= 400

    def test_create_image_for_ml(self):
        pass
