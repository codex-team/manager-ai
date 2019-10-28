import unittest
import httpretty
from transport_telegram import transport_telegram


class TestTransportTelegram(unittest.TestCase):
    """
        Class for testing transport_telegram
    """

    def setUp(self):  # test preparation method
        def request_callback(request, uri, response_headers):  # what answer is right
            ok = request.parsed_body["message"][0] == "Test telegram transport"
            self.assertEqual(ok, True)
            return [200, response_headers, "OK" if ok else "ERROR"]

        httpretty.enable()
        httpretty.register_uri(httpretty.POST, "http://transport_test.com/",
                               body=request_callback)  # register fake http with request_callback

    def tearDown(self):  # final test method
        httpretty.reset()
        httpretty.disable()

    def test_first(self):
        response = transport_telegram("Test telegram transport", "http://transport_test.com/")
        self.assertEqual(response, True)
