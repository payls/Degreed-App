import requests_mock
import json
from fake_data import recommended_course, search_courses, course_list_data, inputs
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
# candidate id
candidate_id = "zk3jPZ"

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


# in fq profile skills and skill goal empty


"""
Given valid term
test that a response returing by this trigger function is correctly as expected
"""


def test_careerhub_entity_search_results_valid_term():
    # update request data with valid term and also update app setting
    event = {}
    request_data = {
        "limit": 10,
        "current_user_email": "payal.sonawane@redcrackle.com",
        "start": 0,
        "term": "Microsoft Office",
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
        # get email from request data
        email = lambda_function.get_email(request_data, app_settings)
        # mock get use id api
        get_userid_return_json = {"data": {"type": "users", "id": "zk3jPZ"}}
        mock.get(
            baseurl + "api/v2/users/" + email + "?identifier=email",
            json=get_userid_return_json,
            status_code=200,
        )
        # get course api call with filter query
        filter_search_term = request_data.get("term")
        url_without_nextBatch = (
            baseurl + "api/v2/content/?filter[term]=" + filter_search_term
        )
        mock.get(
            url_without_nextBatch,
            headers=headers,
            status_code=200,
            json={"data": search_courses.get_data()},
        )
        # set expected response dict
        expected = {
            "entities": course_list_data.get_data(),
            "num_results": 6,
            "limit": 10,
            "offset": 0,
            "cursor": 0,
        }
        # set extected entity schema
        expected_entity_schema = expected.get("entities")[0]
        # calling the function should return filtered course list
        response = lambda_function.careerhub_entity_search_results_handler(
            event, context=""
        )
        response_body = json.loads(response.get("body"))
        response_data = response_body.get("data")
        response_entity_schema = expected.get("entities")[0]
        # to check expected course schema should be equal to entity schema
        check_dict_keys = equal(expected_entity_schema, response_entity_schema)
        # assert statement to check extected and response
        assert check_dict_keys
        assert expected.get("num_results") == response_data.get("num_results")
        assert expected.get("limit") == response_data.get("limit")
        assert expected.get("offset") == response_data.get("offset")
        assert expected.get("cursor") == response_data.get("cursor")


"""
Given valid fq
test that a response returing by this trigger function is correctly as expected
"""


def test_careerhub_entity_search_results_valid_fq():
    # update given request data with valid fq and app setting
    event = {}
    request_data = {
        "limit": 10,
        "current_user_email": "payal.sonawane@redcrackle.com",
        "start": 0,
        "fq": {
            "position_skills": [
                {"name": "Business Strategy"},
                {"name": "Management"},
                {"name": "Software Development"},
                {"name": "Project Management"},
                {"name": "Project Manager"},
                {"name": "AWS"},
                {"name": "Proofing"},
            ],
            "profile_skills": [{"name": "Management"}],
        },
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
        # get email from request data
        email = lambda_function.get_email(request_data, app_settings)
        # mock get use id api
        get_userid_return_json = {"data": {"type": "users", "id": "zk3jPZ"}}
        mock.get(
            baseurl + "api/v2/users/" + email + "?identifier=email",
            json=get_userid_return_json,
            status_code=200,
        )
        # mock recommended courses api
        candidate_id = "zk3jPZ"
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
            skills = {"data": [{"type": "skills", "id": "Project Manager"}]}
            # mock course skills api
            mock.get(
                baseurl + "/api/v2/content/" + course_id + "/skills",
                json=skills,
                headers=headers,
            )
            # fake course details json
            course_details = {
                "data": {
                    "attributes": {
                        "employee-id": None,
                        "language": "en",
                        "assignment-type": "Assigned",
                    }
                }
            }
            # mock course detail api
            mock.get(
                baseurl + "/api/v2/content/" + str(course_id),
                json=course_details,
                headers=headers,
            )

        # filter_search_term = 'Proofing,Business Strategy,Project Management,Project Manager,Software Development,AWS'
        filter_search_term = lambda_function.get_search_string(
            request_data, lambda_function.concate_skills, ""
        )
        # get course api call with filter query
        url_without_nextBatch = (
            baseurl + "api/v2/content/?filter[term]=" + filter_search_term
        )
        mock.get(
            url_without_nextBatch,
            headers=headers,
            status_code=200,
            json={"data": search_courses.get_data()},
        )
        # set expected response dict
        expected = {
            "entities": course_list_data.get_data(),
            "num_results": 7,
            "limit": 10,
            "offset": 0,
            "cursor": 1,
        }
        # set extected entity schema
        expected_entity_schema = expected.get("entities")[0]
        # calling the function which will return filtered course list
        response = lambda_function.careerhub_entity_search_results_handler(
            event, context=""
        )
        response_body = json.loads(response.get("body"))
        response_data = response_body.get("data")
        response_entity_schema = response_data.get("entities")[0]
        # to check expected entity schema and response entity schema is equal or not
        check_dict_keys = equal(expected_entity_schema, response_entity_schema)
        # assert statement to check extected dict and response dict
        assert check_dict_keys
        assert expected.get("num_results") == response_data.get("num_results")
        assert expected.get("limit") == response_data.get("limit")
        assert expected.get("offset") == response_data.get("offset")
        assert expected.get("cursor") == response_data.get("cursor")
