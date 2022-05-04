from helper import resolve_app_path
resolve_app_path()
import lambda_function

"""
Given valid term
test that a response returning by recommendation_trigger_limitations function is equal to expected value
"""


def test_recommendation_trigger_limitations_valid_term():
    # set term
    request_data = {
        "term": "Microsoft Office",
    }
    # set expected
    expected = False
    # calling the function which should return true
    response = lambda_function.recommendation_trigger_limitations(request_data)
    # to check expected is equal to response
    assert expected == response


"""
Given valid trigger_source
test that a response returning by recommendation_trigger_limitations function is equal to expected value
"""


def test_recommendation_trigger_limitations_valid_trigger_source():
    # set trigger source
    request_data = {
        "trigger_source": "ch_jobs",
    }
    # set expected
    expected = False
    # calling the function which should return false
    response = lambda_function.recommendation_trigger_limitations(request_data)
    # to check expected is equal to response
    assert expected == response


"""
Given cursor empty
test that a response returning by recommendation_trigger_limitations function is equal to expected value
"""


def test_recommendation_trigger_limitations_empty_cursor():
    # set trigger source
    request_data = {"trigger_source": "", "cursor": "", "term": ""}
    # set expected
    expected = True
    # calling the function which should return true
    response = lambda_function.recommendation_trigger_limitations(request_data)
    # to check expected is equal to response
    assert expected == response


"""
Given cursor
test that a response returning by recommendation_trigger_limitations function is equal to expected value
"""


def test_recommendation_trigger_limitations_cursor_exists():
    # set trigger source
    request_data = {"trigger_source": "", "cursor": "xyz", "term": ""}
    # set expected
    expected = True
    # calling the function which should return true
    response = lambda_function.recommendation_trigger_limitations(request_data)
    # to check expected is equal to response
    assert expected == response
