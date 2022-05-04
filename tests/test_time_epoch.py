import pytest
from helper import resolve_app_path
resolve_app_path()
import lambda_function

"""
Given date
test that a response returning by time_epoch function is equal as expected
"""


def test_time_epoch_valid_date():
    # set data
    date = "2022-02-16T20:41:20.413"
    # set expected
    expected = 1645044080
    # calling the function which will return date timestamp
    response = lambda_function.time_epoch(date)
    # to check response should be equal to expected
    assert response == expected


"""
Given invalid date
test that a ValueError: raises by calling time_epoch function
"""


def test_time_epoch_invalid_date():
    # set invalid date
    date = "2022-02"
    # to check raises ValueError
    with pytest.raises(ValueError):
        # calling the function which will raises ValueError
        lambda_function.time_epoch(date)


"""
Given empty date
test that a response returning by time_epoch function is empty
"""


def test_time_epoch_empty():
    # set empty date
    date = ""
    # calling the function which will return date timestamp
    response = lambda_function.time_epoch(date)
    # to check response is empty
    assert response == ""
