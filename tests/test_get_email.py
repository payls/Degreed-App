import unittest

from fake_data import inputs
from helper import resolve_app_path
resolve_app_path()
import lambda_function # noqa


# user inputs
inputData = inputs.app()
# request data
request_data = inputData.get("request_data", {})
# app setting
app_settings = inputData.get("app_settings", {})


class GetEmail(unittest.TestCase):
    """
    Given
    use_test_email is valid
    degreed_test_email is valid
    employee_email is empty
    test that a returing email by get_email function should be matched use_test_email
    """
    def test_get_email_true_use_test_email(self):
        # update fake use_test_email in app settings
        app_settings = {
            "use_test_email": True,
            "degreed_test_email": "upendra.tiwari@redcrackle.com",
        }
        # update fake use_test_email in request data
        request_data = {
            "employee_email": "payal.sonawane@redcrackle.com",
        }
        # set expected email
        expected_email = "upendra.tiwari@redcrackle.com"
        # calling the function which will return email
        email = lambda_function.get_email(request_data, app_settings)
        # to check expected email is equal to email
        self.assertEqual(email, expected_email)

    """
    Given
    use_test_email is False
    degreed_test_email is valid
    employee_email is valid
    test that a returing email by get_email function should be matched employee_email
    """
    def test_get_email_false_use_test_email(self):
        # update fake use_test_email in app settings
        app_settings = {
            "use_test_email": False,
            "degreed_test_email": "upendra.tiwari@redcrackle.com",
        }
        # update fake use_test_email in request data
        request_data = {
            "employee_email": "payal.sonawane@redcrackle.com",
        }
        # set expected email
        expected_email = "payal.sonawane@redcrackle.com"
        # calling the function which will return email
        email = lambda_function.get_email(request_data, app_settings)
        # to check expected email is equal to email
        self.assertEqual(email, expected_email)

    """
    Given
    use_test_email is True
    degreed_test_email is empty
    employee_email is valid
    test that a returing email by get_email function should be matched employee_email
    """
    def test_get_email_valid_employee_email(self):
        # update fake use_test_email in app settings
        app_settings = {"use_test_email": True, "degreed_test_email": ""}
        # update fake use_test_email in request data
        request_data = {
            "employee_email": "payal.sonawane@redcrackle.com",
        }
        # set expected email
        expected_email = ""
        # calling the function which will return email
        email = lambda_function.get_email(request_data, app_settings)
        # to check expected email is equal to email
        self.assertEqual(email, expected_email)

    """
    Given
    use_test_email is False
    degreed_test_email is empty
    employee email is empty
    current_user_email is valid
    test that a returing email by get_email function should be matched email
    """
    def test_get_email_blank_employee_email(self):
        # update fake use_test_email in app settings
        app_settings = {"use_test_email": False, "degreed_test_email": ""}
        # update fake use_test_email in request data
        request_data = {
            "employee_email": "",
            "email": "upendra.tiwari@redcrackle.com",
        }
        # set expected email
        expected_email = "upendra.tiwari@redcrackle.com"
        # calling the function which will return email
        email = lambda_function.get_email(request_data, app_settings)
        # to check expected email is equal to email
        self.assertEqual(email, expected_email)

    """
    Given
    use_test_email is False
    degreed_test_email is empty
    email is valid
    test that a returing email by get_email function should be matched email
    """
    def test_get_email_valid_email(self):
        # update fake use_test_email in app settings
        app_settings = {"use_test_email": False, "degreed_test_email": ""}
        # update fake use_test_email in request data
        request_data = {"email": "rajesh.tiwari@redcrackle.com"}
        # set expected email
        expected_email = "rajesh.tiwari@redcrackle.com"
        # calling the function which will return email
        email = lambda_function.get_email(request_data, app_settings)
        # to check expected email is equal to email
        self.assertEqual(email, expected_email)

    """
    Given
    use_test_email is False
    degreed_test_email is empty
    current_user_email is valid
    test that a returing email by get_email function should be matched current_user_email
    """
    def test_get_email_valid_current_user_email(self):
        # update fake use_test_email in app settings
        app_settings = {"use_test_email": False, "degreed_test_email": ""}
        # update fake use_test_email in request data
        request_data = {"current_user_email": "rajesh.tiwari@redcrackle.com"}
        # set expected email
        expected_email = "rajesh.tiwari@redcrackle.com"
        # calling the function which will return email
        email = lambda_function.get_email(request_data, app_settings)
        # to check expected email is equal to email
        self.assertEqual(email, expected_email)
