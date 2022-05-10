import pytest
from unittest.mock import patch
from fake_data import inputs, token_string
from helper import resolve_app_path
resolve_app_path()
import lambda_function # noqa


inputData = inputs.app()
app_settings = inputData.get("app_settings", {})
request_data = inputData.get("request_data", {})
email = lambda_function.get_email(request_data, app_settings)
degreed_base_url = app_settings.get("degreed_base_url")
baseurl = "https://api." + degreed_base_url + "/"
language = app_settings.get("language", "en")
# get token
token_url = "https://" + degreed_base_url
token = token_string.get_token_string()
request_headers = {"Authorization": "Bearer " + str(token)}

"""
Given valid email
test that a candidate_id returning by get_user_id function is equal as given fake candidate_id
"""


def test_get_user_id_valid_email():
    # Mock 'requests' module 'post' method.
    mock_post_patcher = patch("lambda_function.requests.post")
    # Start patching 'requests.post'.
    mock_post = mock_post_patcher.start()
    # Configure the mock to return a response with status code 200.
    mock_post.return_value.status_code = 200
    # Configure the mock to return a response with access token.
    mock_post.return_value.json.return_value = {
        "data": {"type": "users", "id": "zk3jPZ"}
    }
    # Call the function, which will send a request to the server.
    candidate_id = lambda_function.get_user_id(email, baseurl, request_headers)
    # Stop patching 'requests'.
    mock_post_patcher.stop()
    # Assert that the request-response cycle completed successfully.
    assert candidate_id == "zk3jPZ"


"""
Given invalid email
test that a AssertionError raises by calling get_user_id function
"""


def test_get_user_id_invalid_email():
    email = "payal"
    # Mock 'requests' module 'post' method.
    mock_post_patcher = patch("lambda_function.requests.post")
    # Start patching 'requests.post'.
    mock_post = mock_post_patcher.start()
    # Configure the mock to return a response with status code 200.
    mock_post.return_value.status_code = 200
    # Configure the mock to return a response with access token.
    mock_post.return_value.json.return_value = {
        "data": {"type": "users", "id": "zk3jPZ"}
    }
    # Call the function, which will send a request to the server.
    candidate_id = lambda_function.get_user_id(email, baseurl, request_headers)
    # Stop patching 'requests'.
    mock_post_patcher.stop()
    # Assert that the request-response cycle completed successfully.
    with pytest.raises(AssertionError):
        assert candidate_id == "zk3jPZ"


"""
Given empty email
test that a AssertionError raises by calling get_user_id function
"""


def test_get_user_id_empty_email():
    email = ""
    # Mock 'requests' module 'post' method.
    mock_post_patcher = patch("lambda_function.requests.post")
    # Start patching 'requests.post'.
    mock_post = mock_post_patcher.start()
    # Configure the mock to return a response with status code 200.
    mock_post.return_value.status_code = 200
    # Configure the mock to return a response with access token.
    mock_post.return_value.json.return_value = {
        "data": {"type": "users", "id": "zk3jPZ"}
    }
    # Call the function, which will send a request to the server.
    candidate_id = lambda_function.get_user_id(email, baseurl, request_headers)
    # Stop patching 'requests'.
    mock_post_patcher.stop()
    # Assert that the request-response cycle completed successfully.
    with pytest.raises(AssertionError):
        assert candidate_id == "zk3jPZ"
