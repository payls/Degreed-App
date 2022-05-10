from helper import resolve_app_path
resolve_app_path()
import lambda_function # noqa

"""
Given term and skills set
test that a term should be matched with any one skill id
"""


def test_check_with_term_matched():
    # set term
    term = "Microsoft Office"
    # set skills set for match term
    skills = [
        {"type": "skills", "id": "Microsoft Office"},
        {"type": "skills", "id": "Business Strategy"},
    ]
    # calling the function which will return true
    matched = lambda_function.check_with_term(skills, term)
    # check matched true
    assert matched


"""
Given term and skills set
test that a term should not matched with any skill id
"""


def test_check_with_term_not_matched():
    # set term
    term = "Microsoft Office"
    # set skills set for match term
    skills = [
        {"type": "skills", "id": "Project Manager"},
        {"type": "skills", "id": "Business Strategy"},
    ]
    # calling the function which will return true
    matched = lambda_function.check_with_term(skills, term)
    # check matched true
    assert not matched
