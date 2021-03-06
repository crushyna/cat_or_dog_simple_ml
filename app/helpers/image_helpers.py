import logging
from PIL import Image


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
            logging.info("Creating thumbnail image...")
            image = Image.open(image_source_path)
            image.thumbnail((400, 250))
            image.save(image_destination_path)
        except OSError as er:
            return f"Error: {er}"

        return image_destination_path

    @staticmethod
    def create_ml_image(image_source_path: str, image_destination_path: str) -> str:
        """
        Create smaller image of one provided by user.
        This image will be send to ML engine for recognition.
        :param image_source_path: str
        :param image_destination_path: str
        :return: image_destination_path: str
        """
        try:
            logging.info("Creating ML image...")
            image = Image.open(image_source_path)
            image = image.resize((160, 160))
            image.save(image_destination_path)
        except OSError as er:
            return f"Error: {er}"

        return image_destination_path
