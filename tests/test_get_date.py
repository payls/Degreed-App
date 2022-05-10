import pytest
from helper import resolve_app_path
resolve_app_path()
import lambda_function # noqa


"""
Given datetime
test that a response returning by get_date function is equal as expected
"""


def test_get_date_valid_date():
    # set datatime
    datetime = "2022-02-16T20:41:20.413"
    # set expected
    expected = "16/02/2022"
    # calling the function which will return date
    response = lambda_function.get_date(datetime)
    # to check response should be equal to expected
    assert response == expected


"""
Given invalid datetime
test that a ValueError: raises by calling get_date function
"""


def test_get_date_invalid_date():
    # set invalid datetime
    date = "2022-02"
    # to check raises ValueError
    with pytest.raises(ValueError):
        # calling the function which will raises ValueError
        lambda_function.get_date(date)


"""
Given empty datetime
test that a response returning by get_date function is empty
"""


def test_get_date_empty():
    # set empty datetime
    datetime = ""
    # calling the function which will return date timestamp
    response = lambda_function.get_date(datetime)
    # to check response is empty
    assert response == ""
