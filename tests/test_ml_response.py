from models.ml_response import MLResponseClass


class TestMLResponse:
    """
    !!! This tests requires working ML Server !!!
    """
    def test_ml_response_error(self):
        """
        This test asserts that connection is available, and ML server returns information that
        image has incorrect dimensions to be processed.
        """
        test_ml_response = MLResponseClass('cat_example.jpg')
        assert test_ml_response.response['message'] == "input image has incorrect dimensions"
        assert test_ml_response.response['data'] == "none"
        assert test_ml_response.response['status'] == "error"

    def test_ml_response_success(self):
        """
        This test asserts that connection is available, and ML server returns information about
        animal class and raw result data.
        """
        test_ml_response = MLResponseClass('cat_example_160x160.jpg')
        assert test_ml_response.response['message'] == "cat"
        assert isinstance(test_ml_response.response['data'], str) is True
        assert test_ml_response.response['status'] == "success"
