import json
import os
import requests
import logging


class MLResponseClass:
    """
    A class for handling data received from ML Server.
    """

    def __init__(self, ml_filename: str):
        self.ml_filename = ml_filename
        self.ml_server_address = os.getenv('ML_SERVER')
        self.response = self.send_request_to_ml_engine(self.ml_server_address, self.ml_filename)

    @staticmethod
    def send_request_to_ml_engine(ml_server_address: str, image_file: str) -> json:
        """
        Send HTTP request to ML Server instance.
        ML Server address is stored in environment variable 'ML_SERVER' (by default provided by Dockerfile).
        :param ml_server_address: str (from environment variable)
        :param image_file: str (path to it)
        :return: json
        """
        assert os.path.exists(image_file)
        logging.info(f"Uploaded file exists: {os.path.isfile(image_file)}")
        try:
            logging.info(f"Sending request to: {ml_server_address}")
            url = ml_server_address
            payload = open(image_file, 'rb')
            headers = {'Content-Type': 'image/jpeg'}
            response = requests.request("POST", url, headers=headers, data=payload)

        except Exception as er:
            logging.info(er)
            return f"Cannot establish connection to server. {er}"  # this needs proper structure

        logging.info(f"Received response: {response.json()}")
        return response.json()
