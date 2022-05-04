import requests_mock
import json
from fake_data import (
    course_attendance_api_response,
    expected_course_attendance_response,
    inputs,
)
from helper import resolve_app_path
resolve_app_path()
import lambda_function

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
# token_url
token_url = "https://" + degreed_base_url
# language
language = "en"
# get token
token = "-kxz7mYbTrdWL0WYszGf1BHaMYqSnMBp8Fiwak0JRjv5dMoTExxCSGUDkLpTsGM2olF5dns0CcDfFkPOWTNa4zYKJbqDJu5N_TTqL799WIscFWMcvELHZ-xAkU7AU67l5glygzheuJajrZgzvT7il4knjhiKmmvxfBt6pGnorkhxHzVdS60mJbNEgWt1NAngNVeyaRQh087aXpDy-AN5KZDF3VAoGGqxbVB20OmhpjZIhPNSHvVSXS21dynRVPvVTprfpWRtRa4c8BbUryAdcr_BcLRAUAv_rqHWy125UvDn0V_idBEZ48cQZg7-MhxuEceTbMfnS5R3qlzTCkM7fwKMk1QshkmV2xBYyelqi64-4WLzY4yDNW1Y4zPK-n7TlFp-k1IgQUrnXQi4E3LfjhDg_O9IBSNQsBf52Vr4YfONZD_T-FYqEjXIvwmU19tQnZjTfsW88lOMrBuBe1bkx6UxVTU"
# headers
headers = {"Authorization": "Bearer " + str(token)}
email = lambda_function.get_email(request_data, app_settings)

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
Given valid email
test that a response returing by this trigger function is correctly as expected
"""


def test_careerhub_profile_course_attendance_valid_email():
    # update request data with valid email
    event = {}
    request_data = {
        "trigger_name": "careerhub_profile_course_attendance",
        "email": "payal.sonawane@redcrackle.com",
    }
    event.update({"request_data": request_data, "app_settings": app_settings})
    # The Mocker object working as a context manager.
    with requests_mock.Mocker() as mock:
        # mock access token api
        access_token_return_json = {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": 5183999,
            "refresh_token": "4cfc971e671a4cc5afbda32527f6e9c472bdfc6c77c64ee7a6fdc8a2f6e5a54b",
        }
        mock.post(
            token_url + "/oauth/token", json=access_token_return_json, status_code=200
        )

        # mock get use id api
        get_userid_return_json = {"data": {"type": "users", "id": "zk3jPZ"}}
        mock.get(
            baseurl + "api/v2/users/" + email + "?identifier=email",
            json=get_userid_return_json,
            status_code=200,
        )
        # candidate id
        candidate_id = "zk3jPZ"
        # mock api to get profile attendance details
        mock.get(
            baseurl + "/api/v2/users/" + candidate_id + "/completions",
            json={"data": course_attendance_api_response.get_data()},
            headers=headers,
        )
        # set expected course attendance list
        expected = expected_course_attendance_response.get_data()
        expected_profile_schema = expected[0]
        # calling the function should return course attendance list
        response = lambda_function.careerhub_profile_course_attendance_handler(
            event, context=""
        )
        response_body = json.loads(response.get("body"))
        response_data = response_body.get("data")
        response_profile_schema = response_data[0]
        # to check expected course schema should be equal to response course schema
        check_dict_keys = equal(expected_profile_schema, response_profile_schema)
        # check asert statement
        assert check_dict_keys
        assert len(response_data) == len(expected)


"""
Given valid email
test that a response returing by this trigger function is correctly as expected
"""


def test_careerhub_profile_course_attendance_invalid_email():
    # update request data with invalid email
    event = {}
    request_data = {
        "trigger_name": "careerhub_profile_course_attendance",
        "email": "payal.sonaw@redcrackle.com",
    }

    event.update({"request_data": request_data, "app_settings": app_settings})
    # The Mocker object working as a context manager.
    with requests_mock.Mocker() as mock:
        # mock access token api
        access_token_return_json = {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": 5183999,
            "refresh_token": "4cfc971e671a4cc5afbda32527f6e9c472bdfc6c77c64ee7a6fdc8a2f6e5a54b",
        }
        mock.post(
            token_url + "/oauth/token", json=access_token_return_json, status_code=200
        )

        # mock get use id api
        get_userid_return_json = {"data": {"type": "users", "id": "zk3jPZ"}}
        mock.get(
            baseurl + "api/v2/users/" + email + "?identifier=email",
            json=get_userid_return_json,
            status_code=200,
        )
        # candidate id
        candidate_id = "zk3jPZ"

        mock.get(
            baseurl + "/api/v2/users/" + candidate_id + "/completions",
            status_code=404,
            json={"error": "Could not get attendance course detail."},
            headers=headers,
        )

        expected_status_code = 500
        # calling the function should return 500 status code
        response = lambda_function.careerhub_profile_course_attendance_handler(
            event, context=""
        )

        assert response.get("statusCode") == expected_status_code
