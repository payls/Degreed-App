import pytest
from helper import resolve_app_path
resolve_app_path()
import lambda_function


"""
Given url
test that a returing string by course_url_format function should be matched with expected string
"""


def test_course_url_format_with_filter():
    # set url
    url = "https://api.betatest.degreed.com/api/v2/content/?filter[term]=Proofing,Software Development"
    # set expected
    expected = "https://api.betatest.degreed.com/api/v2/content/"
    # calling the function which will return url without
    response_url = lambda_function.course_url_format(url)
    # to check expected url should be equal response url
    assert expected == response_url


"""
Given url
test that a returing string by course_url_format function should be matched with expected string
"""


def test_course_url_format_with_invalid_filter():
    # set url
    url = "https://api.betatest.degreed.com/api/v2/content/?filter[wrong_term]=Proofing,Software Development"
    # set expected
    expected = "https://api.betatest.degreed.com/api/v2/content/"
    # calling the function which will return url without
    response_url = lambda_function.course_url_format(url)
    # Assert that the request-response cycle completed successfully.
    with pytest.raises(AssertionError):
        assert expected == response_url
