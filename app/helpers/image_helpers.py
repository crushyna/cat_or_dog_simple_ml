import os

from PIL import Image
from flask import render_template


class ImageHelpers:
    """
    Simple functions for image compression.
    """

    @staticmethod
    def create_thumbnail(image_source_path: str, image_destination_path: str) -> str:
        """
        Create smaller image of one provided by user.
        This image will be shown on results page.

        :param image_source_path: str
        :param image_destination_path: str
        :return: image_destination_path: str
        """
        try:
            image = Image.open(image_source_path)
            image.thumbnail((400, 400))
            image.save(image_destination_path)
        except OSError as er:
            return f"Error: {er}"

        return image_destination_path
