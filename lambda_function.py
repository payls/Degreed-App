"""
    - Include all dependencies such as Python Standard Modules and open source libraries
"""
from __future__ import absolute_import

import json
import time
import traceback

import concurrent.futures
from datetime import datetime
from datetime import timezone
import requests
import furl


def error_response(error_str):
    """Error Response message"""
    data = {"error": error_str}
    print(json.dumps(data))
    return {"statusCode": 500, "body": json.dumps({"data": data})}


def str2bool(val):
    """Boolean string formatter"""
    return str(val).lower() in ("yes", "true", "t", "1")


def get_access_token(app_settings, token_baseurl):
    """Get Access token from Degreed with Client id & Client Secret"""
    client_id = app_settings.get("degreed_client_id")
    client_secret = app_settings.get("degreed_client_secret")

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "users:read,content:read",
    }
    login_headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # getting token
    response = requests.post(
        token_baseurl + "/oauth/token", headers=login_headers, data=payload
    )

    if response.status_code != 200:
        return error_response("Could not get the token.")

    token = response.json()["access_token"]
    return token


def check_with_term(skills, term):
    """Comparing recommended course skills with term"""
    skill_matched = False
    for skill in skills:
        if skill["id"] == term:
            skill_matched = True
            break
    return skill_matched


def check_with_fq_skills(skills, fq_skills):
    """Comparing recommended course skills with filtered candidate skills"""
    skill_matched = False
    for skill in skills:
        for pskill in fq_skills:
            if pskill.get("name") in skill.get("id").split(";"):
                skill_matched = True
                break
        if skill_matched:
            break
    return skill_matched


def subtract_common_skills(skills_set1, skills_set2):
    """Subtract common skills from required, skill_goals, position or project"""
    uncommon_skills = []
    final_list = list(
        set([s.get("name") for s in skills_set2])
        - set([s.get("name") for s in skills_set1])
    )
    for skill in final_list:
        uncommon_skills.append({"name": skill})

    if not uncommon_skills:
        uncommon_skills = skills_set2
    return uncommon_skills


def concate_skills(str, skills):
    """Comparing content course skills with candidate skills"""
    for skill in skills:
        if str != "":
            str = str + "," + skill.get("name")
        else:
            str = skill.get("name")
    return str


def get_search_string(request_data, skill_function_name, str):
    """Get Filter query/Search Term skills query to fetch or match recommended & content course"""
    term = request_data.get("term")
    if term is not None and term != "":
        if skill_function_name.__name__ == "check_with_fq_skills":
            str = check_with_term(str, term)
        else:
            str = term
    elif "fq" in request_data:
        candidate_skills = request_data.get("fq")
        if candidate_skills is not None and candidate_skills != "":
            profile_skills = candidate_skills.get("profile_skills", [])
            if "position_skills" in candidate_skills:
                position_skills = candidate_skills.get("position_skills", [])
                uncommon_skills = subtract_common_skills(
                    profile_skills, position_skills
                )
                str = skill_function_name(str, uncommon_skills)
            elif "project_skills" in candidate_skills:
                project_skills = candidate_skills.get("project_skills", [])
                uncommon_skills = subtract_common_skills(profile_skills, project_skills)
                str = skill_function_name(str, uncommon_skills)
            elif "skill_goals" in candidate_skills:
                skill_goals = candidate_skills.get("skill_goals", [])
                uncommon_skills = subtract_common_skills(profile_skills, skill_goals)
                str = skill_function_name(str, uncommon_skills)
            elif "required_skills" in candidate_skills:
                required_skills = candidate_skills.get("required_skills", [])
                uncommon_skills = subtract_common_skills(
                    profile_skills, required_skills
                )
                str = skill_function_name(str, uncommon_skills)
            else:
                str = skill_function_name(str, profile_skills)
    elif "skills" in request_data:
        skills = request_data.get("skills")
        str = ",".join(skills)

    return str


def course_url_format(url):
    """Method to remove filter query param if empty"""
    f = furl.furl(url)
    f.remove(["filter[term]"])
    print(f.url)
    return f.url


def get_recommend_skills(baseurl, headers, course):
    """Fetching Skills of recommended course with API call"""
    course_id = course["included"][0]["id"]
    ans = requests.get(
        baseurl + "/api/v2/content/" + course_id + "/skills", headers=headers
    )
    course["skills_status_code"] = ans.status_code
    if ans.status_code != 200:
        print("Could not find skills for course id", course_id)
    else:
        skills_json = ans.json()
        course["skills"] = skills_json["data"]
    return course


def recommend_concurrent_loop(baseurl, headers, recommended_num, recommended_courses):
    """Optimization: Using ThreadPool method to fetch skills using API call for recommended course loop"""
    matching_start_time = time.perf_counter()
    modified_course = []
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=int(recommended_num)
    ) as executor:
        futures = [
            executor.submit(get_recommend_skills, baseurl, headers, course)
            for course in recommended_courses
        ]
    for future in concurrent.futures.as_completed(futures):
        course = future.result()
        modified_course.append(course)
    matching_end_time = time.perf_counter()
    print(
        f"Time taken for fetching course skills concurrent: {matching_end_time - matching_start_time:0.4f} seconds"
    )
    return modified_course


def matching_schema(baseurl, headers, course, language):
    """API call for getting detailed content schema"""
    recomm_course_list = ""
    recommended_course_id = course["included"][0]["id"]
    recommended_course_details_response = requests.get(
        baseurl + "/api/v2/content/" + str(recommended_course_id), headers=headers
    )

    if recommended_course_details_response.status_code != 200:
        print("Could not get recommended required learning details")
    else:
        recomm_course_details_response_json = recommended_course_details_response.json()
        recomm_course_details_item = recomm_course_details_response_json["data"]
        if recomm_course_details_item.get("attributes")["language"] == language:
            recomm_course_list = recomm_course_details_item
    return recomm_course_list


def matching_schema_concurrent_loop(
    baseurl, headers, language, filtered_matched_course_list, recommended_num
):
    """Optimization: Using ThreadPool method for getting detailed schema"""
    matching_schema_start_time = time.perf_counter()
    matched_course_list = []
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=int(recommended_num)
    ) as executor:
        futures = [
            executor.submit(matching_schema, baseurl, headers, course, language)
            for course in filtered_matched_course_list
        ]
    for future in concurrent.futures.as_completed(futures):
        course = future.result()
        if course not in matched_course_list:
            matched_course_list.append(course)
    matching_schema_end_time = time.perf_counter()
    print(
        f"Time taken for fetching course details schema concurrent: {matching_schema_end_time - matching_schema_start_time:0.4f} seconds"
    )
    return matched_course_list


def recommended_course_list(
    baseurl, candidate_id, headers, language, request_data, app_settings
):
    """Get Recommended course list"""
    # recommended courses
    start_time = time.perf_counter()
    trigger_source = request_data.get("trigger_source", "")
    recommended_num = app_settings.get("recommended_course_limit", 5)
    recommended_response = requests.get(
        baseurl + "/api/v2/users/" + candidate_id + "/required-learning",
        headers=headers,
    )
    # print("Required Learning: ", recommended_response.json())
    if recommended_response.status_code != 200:
        return error_response("Could not get recommended courses.")
    recommended_response_json = recommended_response.json()
    recommended_courses = recommended_response_json["data"][: int(recommended_num)]

    count = 1
    skill_matched = False
    filtered_matched_course_list = []
    matched_course_list = []
    # print(recommended_courses)
    if recommended_courses:
        if trigger_source == "ch_search":
            filtered_matched_course_list = recommended_courses
        else:
            print("Fetching skills for recommended courses started")
            modified_course = recommend_concurrent_loop(
                baseurl, headers, recommended_num, recommended_courses
            )
            # Matching skills with request data
            start_time_1 = time.perf_counter()
            for course in modified_course:
                if course["skills_status_code"] == 200:
                    skills = course["skills"]
                    skill_matched = get_search_string(
                        request_data, check_with_fq_skills, skills
                    )

                    if skill_matched:
                        filtered_matched_course_list.append(course)
                        skill_matched = False

                        if count == recommended_num:
                            break
                        count = count + 1

            end_time_1 = time.perf_counter()
            print(
                f"Time taken for matching skills for recommendation: {end_time_1 - start_time_1:0.4f} seconds"
            )

        matched_course_list = matching_schema_concurrent_loop(
            baseurl, headers, language, filtered_matched_course_list, recommended_num
        )

    # print(len(matched_course_list), 'matched_course_list: ', matched_course_list)
    result = {
        "course_list": matched_course_list,
        "course_len": len(matched_course_list),
        "function_name": "recommended_course_list",
    }
    end_time = time.perf_counter()
    print(
        f"Time taken for fetching recommended list: {end_time - start_time:0.4f} seconds"
    )
    return result


def get_search_course_list(baseurl, headers, language, request_data):
    """Get Content course list with filter query parameter"""
    # getting search courses
    start_time = time.perf_counter()
    course_list = []
    course_len = 0
    captured_value = ""

    # if course_count < 10:
    fetch_skill_start_time = time.perf_counter()
    filter_search_term = ""
    search_term = get_search_string(request_data, concate_skills, filter_search_term)
    fetch_skill_end_time = time.perf_counter()
    print(
        f"Time taken for fetching Search query skills: {fetch_skill_end_time - fetch_skill_start_time:0.4f} seconds"
    )

    # Check for Duplicates
    if search_term != "":
        search_words = search_term.split(",")
        filter_search_term = ",".join(sorted(set(search_words), key=search_words.index))

    # remove character from search term
    if len(filter_search_term) > 255:
        filter_search_term = filter_search_term[:255]

    print("Search Term:", filter_search_term)

    # get course api call with filter query
    url_without_nextBatch = (
        baseurl + "api/v2/content/?filter[term]=" + filter_search_term
    )

    # Check for filter query blank
    if filter_search_term == "":
        url_without_nextBatch = course_url_format(url_without_nextBatch)

    course_with_filter_response = requests.get(url_without_nextBatch, headers=headers)
    course_list_response = course_with_filter_response

    if course_list_response.status_code != 200:
        print("Could not get courses")
        course_len = 0
    else:
        course_list_response_json = course_list_response.json()

        # Course List
        filter_course_list = course_list_response_json["data"]
        for course in filter_course_list:
            if course["attributes"]["language"] == language:
                course_list.append(course)
        course_len = len(course_list)

        print("Content searched course count:", course_len)

    result = {
        "course_list": course_list,
        "course_len": course_len,
        "function_name": "get_search_course_list",
        "cursor": captured_value,
    }
    # print(json.dumps(course_list, indent=4))
    end_time = time.perf_counter()
    print(
        f"Time taken for fetching content filter list: {end_time - start_time:0.4f} seconds"
    )
    return result


def get_user_id(email, baseurl, request_headers):
    """Get Degreed candidate id using email as a identifier"""
    user_id = ""
    if email != "" and email is not None:
        candidate_response = requests.get(
            baseurl + "api/v2/users/" + email + "?identifier=email",
            headers=request_headers,
        )
        if candidate_response.status_code != 200:
            print("Could not find the user.")
        else:
            candidate_response_json = candidate_response.json()
            # print(candidate_response_json)
            user_id = candidate_response_json["data"]["id"]

    return user_id


def time_epoch(date):
    """Convert datetime format to time epoch"""
    if date:
        report_completion_date_time = datetime.strptime(
            date.split(".")[0], "%Y-%m-%dT%H:%M:%S"
        )
        date = int(report_completion_date_time.replace(tzinfo=timezone.utc).timestamp())
    return date


def get_date(date):
    """Get date from datetime format"""
    if date:
        course_created_date_time = datetime.strptime(
            date.split(".")[0], "%Y-%m-%dT%H:%M:%S"
        )
        date = course_created_date_time.date().strftime("%d/%m/%Y")
    return date


def get_duration(duration_type, duration):
    """Convert duration of the course in hours - duration types available seconds, minutes, words"""
    if duration_type is None or duration_type == "":
        course_duration = "NA"
    elif duration_type.lower() == "seconds":
        course_duration = round(((duration / 60) / 60), 2)
    elif duration_type.lower() == "minutes":
        course_duration = round(duration / 60, 2)
    elif duration_type.lower() == "words":
        course_duration = round((duration / 250) / 60, 2)
    else:
        course_duration = duration
    return course_duration


def get_image_url(url):
    """Assign degreed logo if image url is empty or unavailable"""
    image_url = url
    if url is None or url == "":
        image_url = "https://blog.degreed.com/wp-content/themes/degreed-blog/assets/img/new-logo.svg"

    return image_url


def get_email(request_data, app_settings):
    """Get candidate/user email - employee_email, email, current_user_email"""
    use_test_email = str2bool(app_settings.get("use_test_email", False))
    degreed_test_email = app_settings.get("degreed_test_email", "")
    email = ""

    employee_email = request_data.get("employee_email", "")
    candidate_email = request_data.get("email", "")
    current_user_email = request_data.get("current_user_email", "")
    if (
        "employee_email" in request_data
        and employee_email != ""
        and employee_email is not None
    ):
        email = degreed_test_email if use_test_email else employee_email
    elif (
        "email" in request_data
        and candidate_email != ""
        and candidate_email is not None
    ):
        email = degreed_test_email if use_test_email else candidate_email
    elif (
        "current_user_email" in request_data
        and current_user_email != ""
        and current_user_email is not None
    ):
        email = degreed_test_email if use_test_email else current_user_email
    elif use_test_email:
        email = degreed_test_email
    print("email:", email)
    return email


def recommendation_trigger_limitations(request_data):
    """Recommendation function calling conditions - Function for adding limitations to recommended course"""
    term = request_data.get("term", "")
    next_batch = request_data.get("cursor")
    trigger_source = request_data.get("trigger_source", "")

    if (
        (term is not None and term != "")
        or trigger_source == "ch_jobs"
        or trigger_source == "ch_projects"
    ):
        return False
    elif next_batch is None or next_batch == "":
        return True
    else:
        return True


def get_combined_concurrent(
    request_data, app_settings, baseurl, candidate_id, request_headers, language
):
    """Optimization: Using ThreadPool method for getting combined courses - Recommendation & content course lists"""
    recomm_list = []
    con_list = []
    course_len = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        print("Parallel ThreadPool start")
        futures = []
        if recommendation_trigger_limitations(request_data):
            futures.append(
                executor.submit(
                    recommended_course_list,
                    baseurl,
                    candidate_id,
                    request_headers,
                    language,
                    request_data,
                    app_settings,
                )
            )
        futures.append(
            executor.submit(
                get_search_course_list, baseurl, request_headers, language, request_data
            )
        )
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            function_name = result.get("function_name")

            if recommendation_trigger_limitations(request_data):
                if function_name == "recommended_course_list":
                    index = 0
                    for item in result.get("course_list"):
                        recomm_list.insert(index, item)
                        index = index + 1
                        course_len = result.get("course_len")

            if function_name == "get_search_course_list":
                course_con_len = result.get("course_len")
                # cursor = result.get('cursor', '')
                for item in result.get("course_list"):
                    con_list.append(item)

        print("Parallel ThreadPool end")

    result = {
        "recomm_list": recomm_list,
        "con_list": con_list,
        "course_len": course_len,
        "course_con_len": course_con_len,
    }

    return result


def recommended_course_cursor_list(
    course_len, endlimit, course_limit, offset, next_batch, recomm_list, con_list
):
    """Course list start & end limit in array function"""
    if course_len >= endlimit:
        recommended_course = recomm_list[offset:endlimit]
    else:
        con_limit = endlimit - course_len
        if course_len >= offset:
            recomm_limit = course_len - offset
            if recomm_limit == 0 or course_len == 0:
                con_list_num = offset - int(0 if next_batch is None else next_batch)
                recommended_course = con_list[
                    con_list_num: (con_list_num + course_limit)
                ]
            else:
                recommended_course = recomm_list[-recomm_limit:] + con_list[:con_limit]
            next_batch = course_len
        else:
            con_list_num = offset - int(0 if next_batch is None else next_batch)
            recommended_course = con_list[con_list_num: (con_list_num + course_limit)]

    result = {"recommended_course": recommended_course, "next_batch": next_batch}

    return result


def get_combined_courses(request_data, app_settings):
    """Get combined course lists"""
    email = get_email(request_data, app_settings)

    degreed_base_url = app_settings.get("degreed_base_url")
    baseurl = "https://api." + degreed_base_url + "/"
    language = app_settings.get("language", "en")
    # get token
    token_url = "https://" + degreed_base_url
    token = get_access_token(app_settings, token_url)
    request_headers = {"Authorization": "Bearer " + str(token)}

    # candidate id
    candidate_id = ""
    start_time = time.perf_counter()
    if email != "":
        candidate_id = get_user_id(email, baseurl, request_headers)
    print("Candidate Id:", candidate_id)
    end_time = time.perf_counter()
    print(f"Time taken for fetching Candidate id: {end_time - start_time:0.4f} seconds")

    next_batch = request_data.get("cursor")

    course_limit = request_data.get("limit", 0)
    if course_limit is None or course_limit == "None":
        course_limit = 0

    offset = request_data.get("start", 0)
    if offset is None or offset == "None":
        offset = 0

    endlimit = offset + course_limit

    if candidate_id == "" or candidate_id is None:
        return error_response("Could not get the courses")
    else:
        recommended_course = []
        get_combined_list = get_combined_concurrent(
            request_data, app_settings, baseurl, candidate_id, request_headers, language
        )
        course_len = get_combined_list.get("course_len")
        course_con_len = get_combined_list.get("course_con_len")
        recomm_list = get_combined_list.get("recomm_list")
        con_list = get_combined_list.get("con_list")

        print("Recommended course count:", course_len)
        recommended_list_cursor = recommended_course_cursor_list(
            course_len,
            endlimit,
            course_limit,
            offset,
            next_batch,
            recomm_list,
            con_list,
        )

        recommended_course = recommended_list_cursor.get("recommended_course")
        next_batch = recommended_list_cursor.get("next_batch")

        # print('recommended_course', recommended_course)
        result = {
            "offset": offset,
            "endlimit": endlimit,
            "course_limit": course_limit,
            "recommended_course_list": recommended_course,
            "recomm_len": course_len,
            "content_len": course_con_len,
            "next_batch": next_batch,
        }

        return result


def careerhub_entity_search_results_handler(event, context):
    """Careerhub Entity Search Results handler"""
    start_handler_time = time.perf_counter()
    request_data = event.get("request_data", {})
    app_settings = event.get("app_settings", {})

    course_list_start_time = time.perf_counter()
    course_list_data = []
    get_combined_course = get_combined_courses(request_data, app_settings)
    if get_combined_course.get("statusCode") == 500:
        return get_combined_course
    else:
        recommended_course = get_combined_course.get("recommended_course_list")
        if recommended_course is not None:
            for course in recommended_course:
                if course != "":
                    course_attr = course.get("attributes", "")
                    course_id = course.get("id", "")
                    course_title = course_attr.get("title", "")
                    course_desc = course_attr.get("summary", "")
                    degreed_url = course_attr.get("degreed-url", "")
                    cta_label = course_attr.get("content-type", "Course")
                    image_url = get_image_url(course_attr.get("image-url", ""))
                    course_modified_at = time_epoch(course_attr.get("modified-at", ""))
                    course_created_at = get_date(course_attr.get("created-at", ""))
                    provider = course_attr.get("provider", "")
                    if provider is None and course_attr.get("is-internal") is True:
                        provider = "Internal"
                    course_duration = get_duration(
                        course_attr.get("duration-type"), course_attr.get("duration")
                    )

                    item = {
                        "entity_id": course_id,
                        "title": course_title,
                        "subtitle": "",
                        "description": course_desc,
                        "custom_fields": "",
                        "last_modified_ts": course_modified_at,
                        "image_url": image_url,
                        "cta_url": degreed_url,
                        "source_name": provider,
                        "fields": [
                            {
                                "name": "Provider",
                                "value": provider,
                            },
                            {
                                "Name": "Durations Hours",
                                "Value": course_duration,
                            },
                            {
                                "name": "Content Type",
                                "value": course_attr.get("content-type", "Course"),
                            },
                            {
                                "name": "Language",
                                "value": course_attr.get("language", ""),
                            },
                            {"name": "Owner", "value": course_attr.get("owner", "")},
                            {"name": "Published Date", "value": course_created_at},
                        ],
                        "cta_label": cta_label,
                        "tags": "",
                        "metadata": "",
                    }

                    course_list_data.append(item)

        content_len = get_combined_course.get("content_len", 0)
        recomm_len = get_combined_course.get("recomm_len", 0)
        course_list_len = int(content_len) + int(recomm_len)

        print("Cursor:", get_combined_course.get("next_batch"))

        data = {
            "entities": course_list_data,
            "num_results": course_list_len,
            "limit": get_combined_course.get("course_limit"),
            "offset": get_combined_course.get("offset"),
            "cursor": get_combined_course.get("next_batch"),
        }

        course_list_end_time = time.perf_counter()
        print(
            f"Time taken for fetching Courses: {course_list_end_time - course_list_start_time:0.4f} seconds"
        )

        # print(data)

        end_handler_time = time.perf_counter()
        print(
            f"Time taken for fetching Handler: {end_handler_time - start_handler_time:0.4f} seconds"
        )

        return {"statusCode": 200, "body": json.dumps({"data": data})}


def careerhub_homepage_recommended_courses_handler(event, context):
    """Careerhub Homepage Recommended Courses handler used in career planner tab"""
    start_handler_time = time.perf_counter()
    request_data = event.get("request_data", {})
    app_settings = event.get("app_settings", {})

    course_list_start_time = time.perf_counter()
    data = []
    get_combined_course = get_combined_courses(request_data, app_settings)
    recommended_course = get_combined_course.get("recommended_course_list")

    # print(recommended_course)
    if recommended_course is not None:
        for course in recommended_course:
            if course != "":
                course_attr = course.get("attributes")
                course_id = course.get("id", "")
                course_title = course_attr.get("title", "")
                course_desc = course_attr.get("summary", "")
                degreed_url = course_attr.get("degreed-url", "")
                cta_label = course_attr.get("content-type")
                image_url = get_image_url(course_attr.get("image-url", ""))
                # course_modified_at = time_epoch(course_attr.get("modified-at", ""))
                time_epoch(course_attr.get("modified-at", ""))
                course_created_at = get_date(course_attr.get("created-at", ""))
                provider = course_attr.get("provider", "")
                if provider is None and course_attr.get("is-internal") is True:
                    provider = "Internal"
                course_duration = get_duration(
                    course_attr.get("duration-type", ""),
                    course_attr.get("duration", ""),
                )
                language = course_attr.get("language", "")

                item = {
                    "status": "",
                    "category": "",
                    "group_id": "",
                    "description": course_desc,
                    "language": language,
                    "title": course_title,
                    "skills": "",
                    "published_date": course_created_at,
                    "lms_course_id": course_id,
                    "lms_data": "",
                    "course_type": cta_label,
                    "image_url": image_url,
                    "provider": provider,
                    "difficulty": "",
                    "course_url": degreed_url,
                    "duration_hours": course_duration,
                }

                data.append(item)

    course_list_end_time = time.perf_counter()
    print(
        f"Time taken for fetching Combined courses: {course_list_end_time - course_list_start_time:0.4f} seconds"
    )

    # print(data)

    end_handler_time = time.perf_counter()
    print(
        f"Time taken for fetching Handler: {end_handler_time - start_handler_time:0.4f} seconds"
    )

    return {"statusCode": 200, "body": json.dumps({"data": data})}


def careerhub_get_entity_details_handler(event, context):
    """Careerhub get Entity Course details"""
    request_data = event.get("request_data", {})
    app_settings = event.get("app_settings", {})

    degreed_base_url = app_settings.get("degreed_base_url")
    baseurl = "https://api." + degreed_base_url + "/"
    # get token
    token_url = "https://" + degreed_base_url
    token = get_access_token(app_settings, token_url)
    request_headers = {"Authorization": "Bearer " + str(token)}

    entity_id = request_data.get("entity_id", 0)
    print(entity_id)

    if entity_id is None or entity_id == "None":
        return error_response("Entity id cannot be blank")

    # getting course details
    course_details_response = requests.get(
        baseurl + "/api/v2/content/" + str(entity_id), headers=request_headers
    )

    if course_details_response.status_code != 200:
        return error_response("Could not get course detail.")

    course_details_response_json = course_details_response.json()
    # print(json.dumps(course_details_response_json, indent=4))

    course_json = course_details_response_json["data"]

    course_attr = course_json.get("attributes", "")

    # Course duration
    course_duration = get_duration(
        course_attr.get("duration-type", ""), course_attr.get("duration", "")
    )

    # Course URL
    degreedUrl = course_attr.get("degreed-url", "")
    cta_url = (
        """<div style="text-align:center;padding:20px 10px;"><a target="_blank"
    style="background-color:#1571ac;padding:10px
    20px;display:inline-block;border-radius:4px;color:#fff;text-decoration:none;" href='"""
        + degreedUrl
        + """'>View
    Course on Degreed</a></div> """
    )

    provider = course_attr.get("provider", "")
    if provider is None and course_attr.get("is-internal") is True:
        provider = "Internal"

    course_modified_at = time_epoch(course_attr.get("modified-at", ""))
    course_created_at = get_date(course_attr.get("created-at", ""))
    last_modified_date = get_date(course_attr.get("modified-at", ""))
    image_url = get_image_url(course_attr.get("image-url", ""))
    owner = course_attr.get("owner") if course_attr.get("owner") else "NA"

    entity_detail = {
        "entity_id": course_json.get("id"),
        "cta_label": course_attr.get("content-type", "Course"),
        "cta_url": degreedUrl,
        "custom_sections": [],
        "description": course_attr.get("summary", "") + " " + cta_url,
        "fields": [
            {"name": "Provider", "value": provider},
            {"name": "Duration Hours", "value": course_duration},
            {
                "name": "Content Type",
                "value": course_attr.get("content-type", "Course"),
            },
            {"name": "Language", "value": course_attr.get("language", "")},
            {"name": "Owner", "value": owner},
            {"name": "Published Date", "value": course_created_at},
            {"name": "Last Modified Date", "value": last_modified_date},
        ],
        "image_url": image_url,
        "last_modified_ts": course_modified_at,
        "metadata": [],
        "source_name": provider,
        "subtitle": "",
        "tags": "",
        "title": course_attr.get("title", ""),
    }

    data = entity_detail

    print(data)

    return {"statusCode": 200, "body": json.dumps({"data": data})}


def careerhub_profile_course_attendance_handler(event, context):
    """Careerhub Profile Course Attendance Handler"""
    request_data = event.get("request_data", {})
    app_settings = event.get("app_settings", {})

    email = get_email(request_data, app_settings)

    degreed_base_url = app_settings.get("degreed_base_url")
    baseurl = "https://api." + degreed_base_url + "/"
    # get token
    token_url = "https://" + degreed_base_url
    token = get_access_token(app_settings, token_url)
    request_headers = {"Authorization": "Bearer " + str(token)}

    # candidate id
    candidate_id = ""
    start_time = time.perf_counter()
    if email != "":
        candidate_id = get_user_id(email, baseurl, request_headers)
    print("Candidate Id:", candidate_id)
    end_time = time.perf_counter()
    print(f"Time taken for fetching Candidate id: {end_time - start_time:0.4f} seconds")

    data = []

    if candidate_id == "" or candidate_id is None:
        return error_response("Could not get completed course's list for a user")
    else:
        course_att_start_time = time.perf_counter()
        course_attendance_response = requests.get(
            baseurl + "/api/v2/users/" + candidate_id + "/completions",
            headers=request_headers,
        )

        if course_attendance_response.status_code != 200:
            return error_response("Could not find course attendance list.")

        course_attendance_response_json = course_attendance_response.json()
        course_list = course_attendance_response_json["data"]
        for course in course_list:
            com_details = course["included"][0]

            course_com_at = time_epoch(course["attributes"]["completed-at"])
            course_added_at = time_epoch(course["attributes"]["added-at"])

            item = {
                "status": "",
                "medium": "",
                "verified": course["attributes"]["is-verified"],
                "description": "",
                "language": "",
                "title": com_details["attributes"]["title"],
                "lms_course_id": com_details["id"],
                "is_internal": com_details["attributes"]["is-internal"],
                "points_earned": course["attributes"]["points-earned"],
                "course_url": com_details["attributes"]["url"],
                "course_type": com_details["attributes"]["content-type"],
                "completion_date": course_com_at,
                "provider": com_details["attributes"]["provider"],
                "data_json": "",
                "difficulty": "",
                "start_date": course_added_at,
            }

            data.append(item)

        course_att_end_time = time.perf_counter()
        print(
            f"Time taken for fetching course attendance list: {course_att_end_time - course_att_start_time:0.4f} seconds"
        )
    # print(data)

    return {"statusCode": 200, "body": json.dumps({"data": data})}


def app_handler(event, context):
    request_data = event.get("request_data", {})
    trigger_name = request_data.get("trigger_name")
    print("Trigger Name: ", trigger_name)
    print("event: ", event)

    try:
        if trigger_name == "careerhub_entity_search_results":
            return careerhub_entity_search_results_handler(event, context)
        elif trigger_name == "careerhub_get_entity_details":
            return careerhub_get_entity_details_handler(event, context)
        elif trigger_name == "career_planner_recommended_courses":
            return careerhub_homepage_recommended_courses_handler(event, context)
        elif trigger_name == "careerhub_profile_course_attendance":
            return careerhub_profile_course_attendance_handler(event, context)
        # elif trigger_name == 'careerhub_get_course_details':
        #     return careerhub_get_course_details_handler(event, context)
        # elif trigger_name == 'careerhub_jobs_recommended_courses':
        #     return careerhub_homepage_recommended_courses_handler(event, context)
        # elif trigger_name == 'careerhub_projects_recommended_courses':
        #     return careerhub_homepage_recommended_courses_handler(event, context)
        # elif trigger_name == 'careerhub_explore_courses':
        #     return careerhub_homepage_recommended_courses_handler(event, context)
        # elif trigger_name == 'careerhub_homepage_recommended_courses':
        #     return careerhub_homepage_recommended_courses_handler(event, context)
        else:
            return error_response("Unknown trigger.")

    except Exception as e:
        data = {}
        error_str = "Something went wrong, traceback: {}".format(traceback.format_exc())
        print(error_str)
        data = {"error": repr(e), "stacktrace": traceback.format_exc()}
        return {"statusCode": 500, "body": json.dumps({"data": data})}
