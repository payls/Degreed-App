import unittest

from helper import resolve_app_path
resolve_app_path()
import lambda_function # noqa


class GetImageUrl(unittest.TestCase):
    """
    Given empty url
    test that a response returning by get_image_url function should be equal to expected
    """
    def test_get_image_url_empty(self):
        # set empty url
        url = ""
        # set expected url
        expected = "https://blog.degreed.com/wp-content/themes/degreed-blog/assets/img/new-logo.svg"
        # calling the function which will return url
        response = lambda_function.get_image_url(url)
        # to check response is equal to expected url
        self.assertEqual(response, response)

    """
    Given None url
    test that a response returning by get_image_url function should be equal to expected
    """
    def test_get_image_url_none(self):
        # set empty url
        url = None
        # set expected url
        expected = "https://blog.degreed.com/wp-content/themes/degreed-blog/assets/img/new-logo.svg"
        # calling the function which will return url
        response = lambda_function.get_image_url(url)
        # to check response is equal to expected url
        self.assertEqual(response, response)


    """
    Given valid url
    test that a response returning by get_image_url function should be equal to expected
    """
    def test_get_image_url_valid(self):
        # set empty url
        url = "https://cdn2.goskills.com/blobs/blogs/126/12-hero.png"
        # set expected url
        expected = "https://cdn2.goskills.com/blobs/blogs/126/12-hero.png"
        # calling the function which will return url
        response = lambda_function.get_image_url(url)
        # to check response is equal to expected url
        self.assertEqual(response, response)
