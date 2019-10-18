import unittest
import requests
import httpretty
from transport_telegram import transport_telegram


class TestTransportTelegram(unittest.TestCase):

    def setUp(self):  # test preparation method
        def request_callback(request, uri, response_headers):  # what answer is right
            ok = request.body == b"message=Test+telegram+transport"
            return [200, response_headers, "OK" if ok else "ERROR"]
        httpretty.enable()
        httpretty.register_uri(httpretty.POST, 'http://transport_test.com/',
                               body=request_callback)  # register fake http

    def tearDown(self):   # final test method
        httpretty.disable()
        httpretty.reset()

    def test_first(self):  # test
        transport_telegram('Test telegram transport', "http://transport_test.com/")  # call our function in face http
        response = requests.post('http://transport_test.com/', data={"message": "Test telegram transport"})
        self.assertEqual(response.text, "OK")

