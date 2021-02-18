import string
import random


class StringHelpers:
    """
    Simple functions for operating on strings.
    """

    @staticmethod
    def generate_random_string(length: int) -> str:
        """
        Create a random string of desired length.
        Used for temporary file naming.
        :param length: int
        :return str
        """
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str
