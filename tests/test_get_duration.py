from helper import resolve_app_path
resolve_app_path()
import lambda_function # noqa

"""
Given duration in seconds
test that a response returning by get_duration function is equal to expected value
"""


def test_get_duration_in_seconds():
    duration_type = "seconds"
    # set fake duration
    duration = 3600
    # set expected
    expected = 1
    # calling the function which will return value in hours
    response = lambda_function.get_duration(duration_type, duration)
    # to check response should be equal to expected
    assert expected == response


"""
Given duration in minutes
test that a response returning by get_duration function is equal to expected value
"""


def test_get_duration_in_minutes():
    duration_type = "minutes"
    # set fake duration
    duration = 120
    # set expected
    expected = 2
    # calling the function which will return value in hours
    response = lambda_function.get_duration(duration_type, duration)
    # to check response should be equal to expected
    assert expected == response


"""
Given duration in words
test that a response returning by get_duration function is equal to expected value
"""


def test_get_duration_in_words():
    duration_type = "words"
    # set duration
    duration = 15000
    # set expected
    expected = 1
    # calling the function which will return value in hours
    response = lambda_function.get_duration(duration_type, duration)
    print("response")
    print(response)
    # to check response should be equal to expected
    assert expected == response
