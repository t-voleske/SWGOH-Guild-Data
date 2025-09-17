from src.helper_functions import (
    get_env,
    check_none_list,
    check_none_str,
    is_list_or_tuple_instance,
    floatify,
)
import os
from dotenv import load_dotenv
from unittest.mock import Mock, patch, ANY
import pytest

@staticmethod
@pytest.fixture
def mock_env_vars():
    env_vars = {
        'PASS': 'password',
        'HOST': 'test_host',
        'USER': 'test_user',
        'DBNAME': 'test_db',
        'PORT': '1235'

    }
    with patch.dict(os.environ, env_vars):
        yield env_vars

def test_get_env(mock_env_vars):
    load_dotenv()
    with pytest.raises(ValueError, match="Error: Check .env file.  should not be None"):
        get_env("")

    assert get_env("DBNAME") == "guild_data"


def test_check_none_list():
    with pytest.raises(
        TypeError,
        match=r"check_none_list\(\) missing 2 required positional arguments: 'possible_none_value' and 'error_str'",
    ):
        check_none_list()

    with pytest.raises(
        TypeError,
        match=r"check_none_list\(\) missing 1 required positional argument: 'error_str'",
    ):
        check_none_list([])

    assert check_none_list([1, 2, 3], "Error string") == [1, 2, 3]
    assert check_none_list([None], "Error string") == [None]

    with pytest.raises(
        TypeError,
        match="possible_none_value should be type list. Use the check_none function of the right type instead!",
    ):
        check_none_list((None,), "Error string")

    with pytest.raises(ValueError, match="This should raise a ValueError"):
        check_none_list(None, "This should raise a ValueError")

    with pytest.raises(ValueError, match="This should also raise a ValueError"):
        check_none_list((None), "This should also raise a ValueError")


def test_check_none_str():
    with pytest.raises(
        TypeError,
        match=r"check_none_str\(\) missing 2 required positional arguments: 'possible_none_value' and 'error_str'",
    ):
        check_none_str()

    with pytest.raises(
        TypeError,
        match=r"check_none_str\(\) missing 1 required positional argument: 'error_str'",
    ):
        check_none_str(
            "One string",
        )

    with pytest.raises(
        TypeError,
        match="possible_none_value should be type str. Use the check_none function of the right type instead!",
    ):
        check_none_str([], "Error String")


def test_is_list_or_tuple_instance():
    with pytest.raises(
        TypeError, match="Input_value is not a list or tuple. Check input_value"
    ):
        is_list_or_tuple_instance("This is not a list or tuple")

    with pytest.raises(
        TypeError,
        match=r"is_list_or_tuple_instance\(\) missing 1 required positional argument: 'input_value'",
    ):
        is_list_or_tuple_instance()

    assert is_list_or_tuple_instance([]) == []
    assert is_list_or_tuple_instance((1,)) == (1,)
    assert is_list_or_tuple_instance([(1,)]) == [(1,)]


def test_floatify():
    assert type(floatify(1)) is float
    assert type(floatify(999999)) is float
    assert type(floatify("")) is str
    assert floatify(2.3) == 2.3
    assert floatify("string") == "-"
    assert floatify("5.5") == 5.5
    assert type(floatify("55")) is float
