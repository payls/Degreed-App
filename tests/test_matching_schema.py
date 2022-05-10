from unittest.mock import patch
import pytest
from fake_data import fake_course, inputs, token_string
from helper import resolve_app_path
resolve_app_path()
import lambda_function # noqa


# user inputs
inputData = inputs.app()
# request data
request_data = inputData.get("request_data", {})
# app setting
app_settings = inputData.get("app_settings", {})
# degree baseurl
degreed_base_url = app_settings.get("degreed_base_url")
# baseurl
baseurl = "https://api." + degreed_base_url + "/"
# language
language = "en"
# get token
token = token_string.get_token_string()
# headers
headers = {"Authorization": "Bearer " + str(token)}

"""
Given course
test that a language returning by matching_schema function is equal as given language
"""


def test_matching_schema_language_matched():
    # set fake course data
    course = fake_course.get_data()
    # get course id for getting course content details
    course_id = course["included"][0]["id"]
    # Mock 'requests' module 'post' method.
    mock_get_patcher = patch("lambda_function.requests.get")
    # Start patching 'requests.get'.
    mock_get = mock_get_patcher.start()
    # Configure the mock to return a response with status code 200.
    mock_get.return_value.status_code = 200
    # Configure the mock to return a response with access token.
    mock_get.return_value.json.return_value = {
        "data": {"type": "content", "id": course_id, "attributes": {"language": "en"}}
    }
    # Call the function, which will send a request to the server.
    response = lambda_function.matching_schema(baseurl, headers, course, language)
    # Stop patching 'requests'.
    mock_get_patcher.stop()
    # to check given language is equal to response course language
    assert response.get("attributes")["language"] == language


"""
Given course
language set invalid
test that a AttributeError raises by calling matching_schema function
"""


def test_matching_schema_language_not_matched():
    # set fake course data
    course = fake_course.get_data()
    # get course id for getting course content details
    course_id = course["included"][0]["id"]
    # Mock 'requests' module 'post' method.
    mock_get_patcher = patch("lambda_function.requests.get")
    # Start patching 'requests.get'.
    mock_get = mock_get_patcher.start()
    # Configure the mock to return a response with status code 200.
    mock_get.return_value.status_code = 200
    # Configure the mock to return a response with access token.
    mock_get.return_value.json.return_value = {
        "data": {"type": "content", "id": course_id, "attributes": {"language": "ku"}}
    }
    # Call the function, which will send a request to the server.
    response = lambda_function.matching_schema(baseurl, headers, course, language)
    # Stop patching 'requests'.
    mock_get_patcher.stop()
    # to check given language is equal to response course language
    with pytest.raises(AttributeError):
        assert response.get("attributes")["language"] == language


"""
Given course with invalid course id
test that a response returning by matching_schema function is empty
"""


def test_matching_schema_invalid_course_id():
    # set fake course data
    course = fake_course.get_data()
    # update wrong course id
    course.update({"included": [{"id": "xyx"}]})
    # Mock 'requests' module 'post' method.
    mock_get_patcher = patch("lambda_function.requests.get")
    # Start patching 'requests.get'.
    mock_get = mock_get_patcher.start()
    # Configure the mock to return a response with status code 200.
    mock_get.return_value.status_code = 404
    # Call the function, which will send a request to the server.
    response = lambda_function.matching_schema(baseurl, headers, course, language)
    # Stop patching 'requests'.
    mock_get_patcher.stop()
    # to check given language is equal to response course language
    assert response == ""
