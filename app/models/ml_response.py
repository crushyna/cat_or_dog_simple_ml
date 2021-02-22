import json
import os
import requests
import logging


class MLResponseClass:
    """
    A class for handling data received from ML Server.
    """

    def __init__(self, filename: str):
        self.original_filename = filename
        self.ml_server_address = os.getenv('ML_SERVER')
        self.response = self.send_request_to_ml_engine(self.ml_server_address, self.original_filename)

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
        logging.info(f"Filepath: {image_file}")
        logging.info(f"File exists: {os.path.exists(image_file)}")
        try:
            logging.info(f"Sending request to: {ml_server_address}")
            url = f"{ml_server_address}"
            payload = image_file
            headers = {'Content-Type': 'image/jpeg'}
            response = requests.request("POST", url, headers=headers, data=payload)

            # logging.info(f"Sending request to: {ml_server_address}")
            # url = f"{ml_server_address}"
            # files = {'file': (open(image_file, 'rb'), 'image/jpeg')}
            # response = requests.post(url=url, files=files)

        except Exception as er:
            return f"Cannot establish connection to server. {er}"  # this needs proper structure

        return response.json()
