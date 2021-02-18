import os

from PIL import Image
from flask import render_template


class ImageHelpers:
    """
    Simple functions for image compression.
    """

    @staticmethod
    def create_thumbnail(image_source_path: str, image_destination_path: str) -> str:
        try:
            image = Image.open(image_source_path)
            image.thumbnail((400, 400))
            image.save(image_destination_path)
        except OSError as er:
            render_template("index.html", error=er)
