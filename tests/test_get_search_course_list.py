from unittest.mock import patch
from fake_data import search_courses, inputs, token_string
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
Given required skills and profile skills
test that a course list returing by get_search_course_list function is correctly
"""


def test_get_search_course_list_based_on_profile_and_required_skills():
    # set fake required_skills and profile_skills
    fq = {
        "required_skills": [
            {"name": "Business Strategy"},
            {"name": "Management"},
            {"name": "Software Development"},
            {"name": "AWS"},
            {"name": "Proofing"},
        ],
        "profile_skills": [{"name": "Management"}],
    }
    # update fake required and profile skills in request data
    request_data.update({"fq": fq, "term": ""})
    fake_data_course_len = 0
    # count matched course with given language
    for course in search_courses.get_data():
        if course["attributes"]["language"] == language:
            fake_data_course_len = fake_data_course_len + 1

    # Mock 'requests' module 'get' method.
    mock_get_patcher = patch("lambda_function.requests.get")
    # Start patching 'requests.post'.
    mock_get = mock_get_patcher.start()
    # Configure the mock to return a response with status code 200.
    mock_get.return_value.status_code = 200
    # Configure the mock to return a response with access token.
    mock_get.return_value.json.return_value = {"data": search_courses.get_data()}
    # Call the function, which will send a request to the server.
    response = lambda_function.get_search_course_list(
        baseurl, headers, language, request_data
    )
    # Stop patching 'requests'.
    mock_get_patcher.stop()
    # Assert that the request-response cycle completed successfully.
    assert fake_data_course_len == response.get("course_len")


"""
Given project skills and profile skills
test that a course list returing by get_search_course_list function is correctly
"""


def test_get_search_course_list_based_on_profile_and_project_skills():
    # set fake project_skills and profile_skills
    fq = {
        "project_skills": [
            {"name": "Business Strategy"},
            {"name": "Management"},
            {"name": "Software Development"},
            {"name": "AWS"},
            {"name": "Proofing"},
        ],
        "profile_skills": [{"name": "Management"}],
    }
    # update fake project and profile skills in request data
    request_data.update({"fq": fq, "term": ""})
    fake_data_course_len = 0
    # count matched course with given language
    for course in search_courses.get_data():
        if course["attributes"]["language"] == language:
            fake_data_course_len = fake_data_course_len + 1

    # Mock 'requests' module 'get' method.
    mock_get_patcher = patch("lambda_function.requests.get")
    # Start patching 'requests.post'.
    mock_get = mock_get_patcher.start()
    # Configure the mock to return a response with status code 200.
    mock_get.return_value.status_code = 200
    # Configure the mock to return a response with access token.
    mock_get.return_value.json.return_value = {"data": search_courses.get_data()}
    # Call the function, which will send a request to the server.
    response = lambda_function.get_search_course_list(
        baseurl, headers, language, request_data
    )
    # Stop patching 'requests'.
    mock_get_patcher.stop()
    # Assert that the request-response cycle completed successfully.
    assert fake_data_course_len == response.get("course_len")


"""
Given goals skills and profile skills
test that a course list returing by get_search_course_list function is correctly
"""


def test_get_search_course_list_based_on_profile_and_skill_goals():
    # set fake position_skills and profile_skills
    fq = {
        "skill_goals": [
            {"name": "Business Strategy"},
            {"name": "Management"},
            {"name": "Software Development"},
            {"name": "AWS"},
            {"name": "Proofing"},
        ],
        "profile_skills": [{"name": "Management"}],
    }
    # update fake goals and profile skills in request data
    request_data.update({"fq": fq, "term": ""})
    fake_data_course_len = 0
    # count matched course with given language
    for course in search_courses.get_data():
        if course["attributes"]["language"] == language:
            fake_data_course_len = fake_data_course_len + 1

    # Mock 'requests' module 'get' method.
    mock_get_patcher = patch("lambda_function.requests.get")
    # Start patching 'requests.post'.
    mock_get = mock_get_patcher.start()
    # Configure the mock to return a response with status code 200.
    mock_get.return_value.status_code = 200
    # Configure the mock to return a response with access token.
    mock_get.return_value.json.return_value = {"data": search_courses.get_data()}
    # Call the function, which will send a request to the server.
    response = lambda_function.get_search_course_list(
        baseurl, headers, language, request_data
    )
    # Stop patching 'requests'.
    mock_get_patcher.stop()
    # Assert that the request-response cycle completed successfully.
    assert fake_data_course_len == response.get("course_len")


"""
Given position skills and profile skills
test that a course list returing by get_search_course_list function is correctly
"""


def test_get_search_course_list_based_on_profile_and_position_skills():
    # set fake position_skills and profile_skills
    fq = {
        "position_skills": [
            {"name": "Business Strategy"},
            {"name": "Management"},
            {"name": "Software Development"},
            {"name": "AWS"},
            {"name": "Proofing"},
        ],
        "profile_skills": [{"name": "Management"}],
    }
    # update fake position and profile skills in request data
    request_data.update({"fq": fq, "term": ""})
    fake_data_course_len = 0
    # count matched course with given language
    for course in search_courses.get_data():
        if course["attributes"]["language"] == language:
            fake_data_course_len = fake_data_course_len + 1

    # Mock 'requests' module 'get' method.
    mock_get_patcher = patch("lambda_function.requests.get")
    # Start patching 'requests.post'.
    mock_get = mock_get_patcher.start()
    # Configure the mock to return a response with status code 200.
    mock_get.return_value.status_code = 200
    # Configure the mock to return a response with access token.
    mock_get.return_value.json.return_value = {"data": search_courses.get_data()}
    # Call the function, which will send a request to the server.
    response = lambda_function.get_search_course_list(
        baseurl, headers, language, request_data
    )
    # Stop patching 'requests'.
    mock_get_patcher.stop()
    # Assert that the request-response cycle completed successfully.
    assert fake_data_course_len == response.get("course_len")
