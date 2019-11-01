import unittest
import httpretty
from scenarios.xpathscenario import XPathScenario

SAMPLE_BODY = r"""
<html>
<head>
  <title>This is a title</title>
</head>
<body>
  <h1>Header 1</h1>
  <p>Paragraph 1</p>
  <p>Paragraph 2</p>
</body>
</html>"""

params_list = [
    {
        "url": "https://test_xpath.com",
        "xpath": "/html/body/h1",
        "answer": "<h1>Header 1</h1>"
    },
    {
        "url": "https://test_xpath.com",
        "xpath": "/html/body/p[1]",
        "answer": "<p>Paragraph 1</p>"
    },
    {
        "url": "https://test_xpath.com",
        "xpath": "/html/body/p[2]",
        "answer": "<p>Paragraph 2</p>"
    },
    {
        "url": "https://test_xpath.com",
        "xpath": "/html/head/title",
        "answer": "<title>This is a title</title>"
    }
]


class TestXPathScenario(unittest.TestCase):
    """A class for testing XPathScenario."""

    def setUp(self) -> None:
        httpretty.enable()
        httpretty.register_uri(httpretty.GET, "https://test_xpath.com",
                               body=SAMPLE_BODY)

    def test_request(self):
        scenario = XPathScenario(params_list[0])
        content = scenario.get_page_content()
        self.assertEqual(SAMPLE_BODY, content)

    def test_getting_element(self):
        for params in params_list:
            scenario = XPathScenario(params)
            element = scenario.get_element(SAMPLE_BODY)
            self.assertEqual(element, params.get("answer"))

    def test_scenario_first_run(self):
        scenario = XPathScenario(params_list[0])
        exists = scenario.run()
        self.assertEqual(exists, False)

    def test_scenario_second_run(self):
        scenario = XPathScenario(params_list[0])
        exists = scenario.run()
        self.assertEqual(exists, True)

    def tearDown(self) -> None:
        httpretty.disable()
        httpretty.reset()


if __name__ == "__main__":
    unittest.main()
