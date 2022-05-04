from helper import resolve_app_path
resolve_app_path()
import lambda_function

"""
Given profile skills and other skills set
test that a returning skills set by subtract_common_skills function should not have any profile skill
"""


def test_subtract_common_skills_uncommon():
    # set profile skills
    profile_skills = [{"name": "Management"}]
    # set other skills
    other_skills = [
        {"name": "Business Strategy"},
        {"name": "Management"},
        {"name": "Software Development"},
        {"name": "Project Management"},
        {"name": "Frameworks"},
        {"name": "Design Analysis"},
    ]
    # expected skills set
    expected_skills = [
        {"name": "Business Strategy"},
        {"name": "Software Development"},
        {"name": "Project Management"},
        {"name": "Frameworks"},
        {"name": "Design Analysis"},
    ]
    # calling the function which will return skills set
    uncommon_skills = lambda_function.subtract_common_skills(
        profile_skills, other_skills
    )

    # to check expected skills and uncommon skill is equal
    matched = True
    for skill in expected_skills:
        if skill not in uncommon_skills:
            matched = False
    assert matched
    # check length of expected skills and length of un common skills
    assert len(expected_skills) == len(uncommon_skills)


"""
Given profile skills and other skills set
test that a returning skills set by subtract_common_skills function should not have any profile skill
"""


def test_subtract_common_skills_empty_other_skills():
    # set profile skills
    profile_skills = [{"name": "Management"}]
    # set other skills
    other_skills = []
    # expected skills set
    expected_skills = []
    # calling the function which will return skills set
    uncommon_skills = lambda_function.subtract_common_skills(
        profile_skills, other_skills
    )

    # to check expected skills and uncommon skill is equal
    matched = True
    for skill in expected_skills:
        if skill not in uncommon_skills:
            matched = False
    assert matched
    # check length of expected skills and length of un common skills
    assert len(expected_skills) == len(uncommon_skills)


"""
Given profile skills and other skills set
test that a returning skills set by subtract_common_skills function should not have any profile skill
"""


def test_subtract_common_skills_profile_akills_empty():
    # set profile skills
    profile_skills = []
    # set other skills
    other_skills = [
        {"name": "Business Strategy"},
        {"name": "Management"},
        {"name": "Software Development"},
        {"name": "Project Management"},
        {"name": "Frameworks"},
        {"name": "Design Analysis"},
    ]
    # expected skills set
    expected_skills = [
        {"name": "Business Strategy"},
        {"name": "Management"},
        {"name": "Software Development"},
        {"name": "Project Management"},
        {"name": "Frameworks"},
        {"name": "Design Analysis"},
    ]
    # calling the function which will return skills set
    uncommon_skills = lambda_function.subtract_common_skills(
        profile_skills, other_skills
    )

    # to check expected skills and uncommon skill is equal
    matched = True
    for skill in expected_skills:
        if skill not in uncommon_skills:
            matched = False
    assert matched
    # check length of expected skills and length of un common skills
    assert len(expected_skills) == len(uncommon_skills)
