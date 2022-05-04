from helper import resolve_app_path
resolve_app_path()
import lambda_function

"""
Given empty str and array of skills
test that a returing string by get_email function should be matched with expected string
"""


def test_concate_skills_empty_str():
    # set empty str
    str = ""
    # set array of skills
    skills = [
        {"name": "Business Strategy"},
        {"name": "Management"},
        {"name": "Software Development"},
        {"name": "Project Management"},
        {"name": "Frameworks"},
    ]
    # set expected string
    expected = "Business Strategy,Management,Software Development,Project Management,Frameworks"
    # calling the function which will return concat string
    concat_str = lambda_function.concate_skills(str, skills)
    # to check concat str is equal to expected
    assert expected == concat_str


"""
Given str and array of skills
test that a returing string by get_email function should be matched with expected string
"""


def test_concate_skills():
    # set empty str
    str = "Soft Skills"
    # set array of skills
    skills = [
        {"name": "Business Strategy"},
        {"name": "Management"},
        {"name": "Software Development"},
        {"name": "Project Management"},
        {"name": "Frameworks"},
    ]
    # set expected string
    expected = "Soft Skills,Business Strategy,Management,Software Development,Project Management,Frameworks"
    # calling the function which will return concat string
    concat_str = lambda_function.concate_skills(str, skills)
    # to check concat str is equal to expected
    assert expected == concat_str
