from helper import resolve_app_path
resolve_app_path()
import lambda_function

"""
Given skills and fq skills set
test that a any skill id should be matched with any fq skill
"""


def test_check_with_fq_skills_matched_ckill():
    # set skills set
    skills = [
        {"type": "skills", "id": "Project Manager"},
        {"type": "skills", "id": "Business Strategy"},
    ]
    # set fq_skills set
    fq_skills = [{"name": "Business Strategy"}, {"name": "Management"}]
    # calling the function which will return true
    matched = lambda_function.check_with_fq_skills(skills, fq_skills)
    # check matched true
    assert matched


"""
Given skills and fq skills set
test that a skill id should not matched with any fq skill
"""


def test_check_with_fq_skills_not_matched_skill():
    # set skills set
    skills = [
        {"type": "skills", "id": "Project Manager"},
        {"type": "skills", "id": "Business Strategy"},
    ]
    # set fq_skills set
    fq_skills = [{"name": "Software Development"}, {"name": "Management"}]
    # calling the function which will return true
    matched = lambda_function.check_with_fq_skills(skills, fq_skills)
    # check matched true
    assert not matched
