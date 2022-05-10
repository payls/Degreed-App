import requests_mock
from fake_data import recommended_course, inputs, search_courses, token_string
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
# token_url
token_url = "https://" + degreed_base_url
# language
language = "en"
# get token
token = token_string.get_token_string()
# headers
headers = {"Authorization": "Bearer " + str(token)}
# candidate id
candidate_id = "zk3jPZ"
email = lambda_function.get_email(request_data, app_settings)


def test_get_combined_courses_valid_term():
    request_data = {
        "limit": 10,
        "current_user_email": "payal.sonawane@redcrackle.com",
        "start": 0,
        "term": "Microsoft Office",
    }

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

        filter_search_term = "Microsoft Office"
        request_data.update({"term": "Microsoft Office"})

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

        expected = {
            "offset": 0,
            "endlimit": 10,
            "course_limit": 10,
            "recommended_course_list": recommended_course.get_data(),
            "recomm_len": 0,
            "content_len": 6,
            "next_batch": 0,
        }
        response = lambda_function.get_combined_courses(request_data, app_settings)

        assert expected.get("offset") == response.get("offset")
        assert expected.get("endlimit") == response.get("endlimit")
        assert expected.get("course_limit") == response.get("course_limit")
        assert expected.get("recomm_len") == response.get("recomm_len")
        assert expected.get("content_len") == response.get("content_len")
        assert expected.get("next_batch") == response.get("next_batch")


def test_get_combined_courses_invalid_term():
    request_data = {
        "limit": 10,
        "current_user_email": "payal.sonawane@redcrackle.com",
        "start": 0,
        "term": "xyz",
    }

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

        filter_search_term = "xyz"
        request_data.update({"term": filter_search_term})

        # get course api call with filter query
        url_without_nextBatch = (
            baseurl + "api/v2/content/?filter[term]=" + filter_search_term
        )
        mock.get(
            url_without_nextBatch, headers=headers, status_code=200, json={"data": []}
        )

        expected = {
            "offset": 0,
            "endlimit": 10,
            "course_limit": 10,
            "recommended_course_list": 0,
            "recomm_len": 0,
            "content_len": 0,
            "next_batch": 0,
        }
        response = lambda_function.get_combined_courses(request_data, app_settings)

        assert expected.get("offset") == response.get("offset")
        assert expected.get("endlimit") == response.get("endlimit")
        assert expected.get("course_limit") == response.get("course_limit")
        assert expected.get("recomm_len") == response.get("recomm_len")
        assert expected.get("content_len") == response.get("content_len")
        assert expected.get("next_batch") == response.get("next_batch")


def test_get_combined_courses_valid_fq():
    request_data = {
        "limit": 10,
        "current_user_email": "payal.sonawane@redcrackle.com",
        # "trigger_source": "ch_homepage",  # ch_career_planner, ch_search, ch_jobs, ch_projects, ch_homepage
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

        expected = {
            "offset": 0,
            "endlimit": 10,
            "course_limit": 10,
            "recommended_course_list": recommended_course.get_data(),
            "recomm_len": 1,
            "content_len": 6,
            "next_batch": 1,
        }
        response = lambda_function.get_combined_courses(request_data, app_settings)

        assert expected.get("offset") == response.get("offset")
        assert expected.get("endlimit") == response.get("endlimit")
        assert expected.get("course_limit") == response.get("course_limit")
        assert expected.get("recomm_len") == response.get("recomm_len")
        assert expected.get("content_len") == response.get("content_len")
        assert expected.get("next_batch") == response.get("next_batch")
