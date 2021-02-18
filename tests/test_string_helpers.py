import pytest
from helpers.string_helpers import StringHelpers


class TestStringHelpers:
    def test_generate_random_string_1(self):
        result = StringHelpers.generate_random_string(5)
        assert len(result) == 5

    def test_generate_random_string_2(self):
        with pytest.raises(TypeError):
            result = StringHelpers.generate_random_string(9, 5)

    def test_generate_random_string_3(self):
        with pytest.raises(TypeError):
            result = StringHelpers.generate_random_string(9.5)

    def test_generate_random_string_4(self):
        result = StringHelpers.generate_random_string(-5)
        assert len(result) == 0
