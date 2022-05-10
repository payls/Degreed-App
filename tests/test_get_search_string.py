from fake_data import inputs
from helper import resolve_app_path
resolve_app_path()
import lambda_function # noqa


inputData = inputs.app()
request_data = inputData.get("request_data", {})

"""
Given matched term with course skill
test that a skill matched by calling get_search_string function
"""


def test_get_search_string_skill_matched():
    # set term with request data
    request_data.update({"term": "Microsoft Office"})
    # set skills set for match term
    skills = [{"type": "skills", "id": "Microsoft Office"}]
    # calling the function which will return true
    skill_matched = lambda_function.get_search_string(
        request_data, lambda_function.check_with_fq_skills, skills
    )
    # assert skill matched true
    assert skill_matched


"""
Given unmatched term with course skill
test that a skill not matched by calling get_search_string function
"""


def test_get_search_string_skill_not_matched():
    # set term with request data
    request_data.update({"term": "Software Development"})
    # set skills set for match term
    skills = [{"type": "skills", "id": "Microsoft Office"}]
    # calling the function which will return False
    skill_matched = lambda_function.get_search_string(
        request_data, lambda_function.check_with_fq_skills, skills
    )
    # assert skill not matched
    assert not skill_matched


"""
Given term
test that a returing skill by calling get_search_string function should be equal of term
"""


def test_get_search_string_concate_skills():
    # set term with request data
    term = "Microsoft Office"
    request_data.update({"term": term})
    # calling the function which will return treu or false
    skill = lambda_function.get_search_string(
        request_data, lambda_function.concate_skills, term
    )
    # assert skill matched or not
    assert skill == term


"""
Given required skills and profile skills
test that a search string returing by get_search_string function is correctly
"""


def test_get_search_string_of_profile_and_required_skills():
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
    # set expected skills
    expected_terms = ["Business Strategy", "AWS", "Software Development", "Proofing"]

    filter_search_term = ""
    # calling the function which will return search terms
    search_term = lambda_function.get_search_string(
        request_data, lambda_function.concate_skills, filter_search_term
    )
    # split search terms into array
    search_terms_arr = search_term.split(",")

    # to check expected_terms and search_terms_arr values are same
    matched = True
    for expected_skill in expected_terms:
        if expected_skill not in search_terms_arr:
            matched = False
    assert matched

    # assert lenght of expected_terms and search_terms_arr is equal
    assert len(expected_terms) == len(search_terms_arr)


"""
Given project skills and profile skills
test that a search string returing by get_search_string function is correctly
"""


def test_get_search_string_of_profile_and_project_skills():
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
    # set expected skills
    expected_terms = ["Business Strategy", "AWS", "Software Development", "Proofing"]

    filter_search_term = ""
    # calling the function which will return search terms
    search_term = lambda_function.get_search_string(
        request_data, lambda_function.concate_skills, filter_search_term
    )
    # split search terms into array
    search_terms_arr = search_term.split(",")

    # to check expected_terms and search_terms_arr values are same
    matched = True
    for expected_skill in expected_terms:
        if expected_skill not in search_terms_arr:
            matched = False
    assert matched

    # assert lenght of expected_terms and search_terms_arr is equal
    assert len(expected_terms) == len(search_terms_arr)


"""
Given goals skill and profile skills
test that a search string returing by get_search_string function is correctly
"""


def test_get_search_string_of_profile_and_goals_skills():
    # set fake skill_goals and profile_skills
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
    # set expected skills
    expected_terms = ["Business Strategy", "AWS", "Software Development", "Proofing"]

    filter_search_term = ""
    # calling the function which will return search terms
    search_term = lambda_function.get_search_string(
        request_data, lambda_function.concate_skills, filter_search_term
    )
    # split search terms into array
    search_terms_arr = search_term.split(",")

    # to check expected_terms and search_terms_arr values are same
    matched = True
    for expected_skill in expected_terms:
        if expected_skill not in search_terms_arr:
            matched = False
    assert matched

    # assert lenght of expected_terms and search_terms_arr is equal
    assert len(expected_terms) == len(search_terms_arr)


"""
Given position skills and profile skills
test that a search string returing by get_search_string function is correctly
"""


def test_get_search_string_of_profile_and_position_skills():
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
    # set expected skills
    expected_terms = ["Business Strategy", "AWS", "Software Development", "Proofing"]

    filter_search_term = ""
    # calling the function which will return search terms
    search_term = lambda_function.get_search_string(
        request_data, lambda_function.concate_skills, filter_search_term
    )
    # split search terms into array
    search_terms_arr = search_term.split(",")

    # to check expected_terms and search_terms_arr values are same
    matched = True
    for expected_skill in expected_terms:
        if expected_skill not in search_terms_arr:
            matched = False
    assert matched

    # assert lenght of expected_terms and search_terms_arr is equal
    assert len(expected_terms) == len(search_terms_arr)


"""
Given profile skills
test that a search string returing by get_search_string function is correctly
"""


def test_get_search_string_of_profile_skills():
    # set fake profile_skills
    fq = {"profile_skills": [{"name": "Management"}, {"name": "Business Strategy"}]}
    # update fake profile skills in request data
    request_data.update({"fq": fq, "term": ""})
    # set expected skills
    expected_terms = "Management,Business Strategy"

    filter_search_term = ""
    # calling the function which will return search terms
    search_term = lambda_function.get_search_string(
        request_data, lambda_function.concate_skills, filter_search_term
    )

    # assert expected_terms and search_term is equal
    assert expected_terms == search_term


"""
Given skills
test that a search string returing by get_search_string function is correctly
"""


def test_get_search_string_of_skills():
    # set fake skills
    skills = {"skills": [{"name": "Management"}, {"name": "Business Strategy"}]}
    # update fake profile skills in request data
    request_data.update(skills)
    # set expected skills
    expected_terms = "Management,Business Strategy"

    filter_search_term = ""
    # calling the function which will return search terms
    search_term = lambda_function.get_search_string(
        request_data, lambda_function.concate_skills, filter_search_term
    )

    # assert expected_terms and search_term is equal
    assert expected_terms == search_term
