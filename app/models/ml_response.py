import os
import tensorflow as tf


class MLResponseClass:
    """
    A class for handling data received from ML Server.
    """

    def __init__(self, filename: str):
        self.original_filename = filename
        self.image_array = generate_image_array(filename)
        self.ml_server_address = os.environ.get('ML_SERVER')
        self.response: tf.tensor

