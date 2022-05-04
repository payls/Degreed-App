from helper import resolve_app_path
resolve_app_path()
import lambda_function

"""
Given endlimit, next_batch, offset, course_limit, course_len, recomm_list, con_list
test that a response returning by recommended_course_cursor_list function is equal as expected
"""


def test_recommended_course_cursor_list():
    # set fake input data
    endlimit = 10
    next_batch = 0
    offset = 0
    course_limit = 10
    course_len = 8
    recomm_list = [
        {"type": "required-learning"},
        {"type": "required-learning"},
        {"type": "required-learning"},
        {"type": "required-learning"},
        {"type": "required-learning"},
        {"type": "required-learning"},
        {"type": "required-learning"},
        {"type": "required-learning"},
    ]
    con_list = [
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
    ]

    # set expected
    expected_next_batch = 8
    expected_recommended_course_len = 8
    expected_content_course_len = 2
    # calling the function which will return recommended_list and cursor
    recommended_list_cursor = lambda_function.recommended_course_cursor_list(
        course_len, endlimit, course_limit, offset, next_batch, recomm_list, con_list
    )

    # assert statement to check expected and response values
    response_recommended_course_len = 0
    response_content_course_len = 0
    response_next_batch = recommended_list_cursor.get("next_batch")
    for course in recommended_list_cursor.get("recommended_course"):
        if course.get("type") == "required-learning":
            response_recommended_course_len = response_recommended_course_len + 1
        if course.get("type") == "content":
            response_content_course_len = response_content_course_len + 1

    assert expected_next_batch == response_next_batch
    assert expected_recommended_course_len == response_recommended_course_len
    assert expected_content_course_len == response_content_course_len


"""
Given endlimit, next_batch, offset, course_limit, course_len, recomm_list, con_list
test that a response returning by recommended_course_cursor_list function is equal as expected
"""


def test_recommended_course_cursor_list_recomm_list():
    # set fake input data
    endlimit = 10
    next_batch = 0
    offset = 0
    course_limit = 10
    course_len = 12
    recomm_list = [
        {"type": "required-learning"},
        {"type": "required-learning"},
        {"type": "required-learning"},
        {"type": "required-learning"},
        {"type": "required-learning"},
        {"type": "required-learning"},
        {"type": "required-learning"},
        {"type": "required-learning"},
        {"type": "required-learning"},
        {"type": "required-learning"},
        {"type": "required-learning"},
        {"type": "required-learning"},
    ]
    con_list = [
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
        {"type": "content"},
    ]

    # set expected
    expected_next_batch = 0
    expected_recommended_course_len = 10
    expected_content_course_len = 0
    # calling the function which will return recommended_list and cursor
    recommended_list_cursor = lambda_function.recommended_course_cursor_list(
        course_len, endlimit, course_limit, offset, next_batch, recomm_list, con_list
    )

    # assert statement to check expected and response values
    response_recommended_course_len = 0
    response_content_course_len = 0
    response_next_batch = recommended_list_cursor.get("next_batch")
    for course in recommended_list_cursor.get("recommended_course"):
        if course.get("type") == "required-learning":
            response_recommended_course_len = response_recommended_course_len + 1
        if course.get("type") == "content":
            response_content_course_len = response_content_course_len + 1

    assert expected_next_batch == response_next_batch
    assert expected_recommended_course_len == response_recommended_course_len
    assert expected_content_course_len == response_content_course_len

    print("recommended_list_cursor")
    print(recommended_list_cursor)
