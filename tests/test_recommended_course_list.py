import requests_mock
from fake_data import (
    recommended_course,
    inputs,
    token_string,
    entity_details,
    course_matched_list,
)
from helper import resolve_app_path

resolve_app_path()
import lambda_function  # noqa

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
to check twp dict is equal or not
"""


def equal(a, b):
    type_a = type(a)
    type_b = type(b)

    if type_a != type_b:
        return False

    if isinstance(a, dict):
        if len(a) != len(b):
            return False
        for key in a:
            if key not in b:
                return False
        return True


"""
test recommended course for valid candidate id.
"""


def test_recommended_course_list_valid_candidate_id():
    # candidate id
    candidate_id = "zk3jPZ"

    # The Mocker object working as a context manager.
    with requests_mock.Mocker() as mock:
        # mock recommended course api
        # input - valid candidate id
        # expected response - status code 200 and return value json
        mock.get(
            baseurl + "/api/v2/users/" + candidate_id + "/required-learning",
            headers=headers,
            json={"data": recommended_course.get_data()},
        )
        # fake recommended courses
        recommended_courses = recommended_course.get_data()
        # traverse fake recommended courses
        for course in recommended_courses:
            # parse course id from course
            course_id = course["included"][0]["id"]
            # fake skills json
            skills = {"data": [{"type": "skills", "id": "Software Development"}]}
            # mock course skills api
            mock.get(
                baseurl + "/api/v2/content/" + course_id + "/skills",
                json=skills,
                headers=headers,
            )

            # fake course details json
            course_details = entity_details.get_data()
            # mock course detail api
            mock.get(
                baseurl + "/api/v2/content/" + str(course_id),
                json=course_details,
                headers=headers,
            )

        expected = {
            "course_list": course_matched_list.get_data(),
            "course_len": len(course_matched_list.get_data()),
            "function_name": "recommended_course_list",
        }
        # set extected course schema
        expected_course_schema = expected.get("course_list")[0]
        # calling recommended courses function
        response = lambda_function.recommended_course_list(
            baseurl, candidate_id, headers, language, request_data, app_settings
        )
        response_course_schema = response.get("course_list")[0]
        # to check expected course schema should be equal to response course schema
        check_dict_keys = equal(expected_course_schema, response_course_schema)
        # assert statement to check extected and response
        assert check_dict_keys
        assert len(expected.get("course_list")) == len(response.get("course_list"))


"""
test recommended course for invalid candidate id.
"""


def test_recommended_course_list_invalid_candidate_id():
    # make candidate id invalid
    candidate_id = "xyz"
    # The Mocker object working as a context manager.
    with requests_mock.Mocker() as mock:
        # set invalid candidate id
        candidate_id = "xyz"
        # mock recommended course api
        # input - invalid candidate id
        # expected response - status code 404 and error message
        mock.get(
            baseurl + "/api/v2/users/" + candidate_id + "/required-learning",
            headers=headers,
            status_code=404,
            json={"error": "Could not get recommended courses."},
        )
        # calling recommended courses function
        response = lambda_function.recommended_course_list(
            baseurl, candidate_id, headers, language, request_data, app_settings
        )
        # to check response status code
        assert response.get("statusCode") == 500


"""
test recommended course for empty candidate id.
"""


def test_recommended_course_list_empty_candidate_id():
    # make candidate id empty
    candidate_id = ""
    # The Mocker object working as a context manager.
    with requests_mock.Mocker() as mock:
        # set invalid candidate id
        candidate_id = "xyz"
        # mock recommended course api
        # input - empty candidate id
        # expected response - status code 404 and error message
        mock.get(
            baseurl + "/api/v2/users/" + candidate_id + "/required-learning",
            headers=headers,
            status_code=404,
            json={"error": "Could not get recommended courses."},
        )

        # calling recommended courses function
        response = lambda_function.recommended_course_list(
            baseurl, candidate_id, headers, language, request_data, app_settings
        )
        # to check response status code 500
        assert response.get("statusCode") == 500
