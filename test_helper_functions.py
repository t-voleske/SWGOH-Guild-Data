from helper_functions import (
    get_env,
    check_none_list,
    check_none_str,
    is_list_or_tuple_instance,
)
import pytest


def test_get_env():
    with pytest.raises(
        ValueError, match="Error: Check .env file. %s should not be None"
    ):
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


def test_is_ist_or_tuple_instance():
    with pytest.raises(
        TypeError, match="Input is not a list or tuple. Check input function!"
    ):
        is_list_or_tuple_instance("This is not a list or tuple")

    with pytest.raises(
        TypeError,
        match=r"is_list_or_tuple_instance\(\) missing 1 required positional argument: 'input'",
    ):
        is_list_or_tuple_instance()

    assert is_list_or_tuple_instance([]) == []
    assert is_list_or_tuple_instance((1,)) == (1,)
    assert is_list_or_tuple_instance([(1,)]) == [(1,)]
