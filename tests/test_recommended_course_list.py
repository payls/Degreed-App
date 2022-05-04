import requests_mock
from fake_data import recommended_course, inputs
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
# language
language = "en"
# get token
token = "-kxz7mYbTrdWL0WYszGf1BHaMYqSnMBp8Fiwak0JRjv5dMoTExxCSGUDkLpTsGM2olF5dns0CcDfFkPOWTNa4zYKJbqDJu5N_TTqL799WIscFWMcvELHZ-xAkU7AU67l5glygzheuJajrZgzvT7il4knjhiKmmvxfBt6pGnorkhxHzVdS60mJbNEgWt1NAngNVeyaRQh087aXpDy-AN5KZDF3VAoGGqxbVB20OmhpjZIhPNSHvVSXS21dynRVPvVTprfpWRtRa4c8BbUryAdcr_BcLRAUAv_rqHWy125UvDn0V_idBEZ48cQZg7-MhxuEceTbMfnS5R3qlzTCkM7fwKMk1QshkmV2xBYyelqi64-4WLzY4yDNW1Y4zPK-n7TlFp-k1IgQUrnXQi4E3LfjhDg_O9IBSNQsBf52Vr4YfONZD_T-FYqEjXIvwmU19tQnZjTfsW88lOMrBuBe1bkx6UxVTU"
# headers
headers = {"Authorization": "Bearer " + str(token)}
# candidate id
candidate_id = "zk3jPZ"


"""
test recommended course for valid candidate id.
"""


def test_recommended_course_list_valid_candidate_id():
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
            skills = {
                "data": [{"type": "skills", "id": "Microsoft Excel;Microsoft Office"}]
            }
            # mock course skills api
            mock.get(
                baseurl + "/api/v2/content/" + course_id + "/skills",
                json=skills,
                headers=headers,
            )

            # fake course details json
            course_details = {
                "attributes": {
                    "employee-id": None,
                    "language": "en",
                    "assignment-type": "Assigned",
                }
            }
            # mock course detail api
            mock.get(
                baseurl + "/api/v2/content/" + str(course_id),
                json=course_details,
                headers=headers,
            )
        # calling recommended courses function
        lambda_function.recommended_course_list(
            baseurl, candidate_id, headers, language, request_data, app_settings
        )


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
