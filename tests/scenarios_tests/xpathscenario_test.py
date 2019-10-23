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
        "xpath": "/html/body/h1"
    },
    {
        "url": "https://test_xpath.com",
        "xpath": "/html/body/p[1]"
    },
    {
        "url": "https://test_xpath.com",
        "xpath": "/html/body/p[2]"
    },
    {
        "url": "https://test_xpath.com",
        "xpath": "/html/head/title"
    }
]


class TestXPathScenario(unittest.TestCase):
    def setUp(self) -> None:
        httpretty.enable()
        httpretty.register_uri(httpretty.GET, "https://test_xpath.com",
                               body=SAMPLE_BODY)

    def test_xpath_scenario(self):
        for params in params_list:
            scenario = XPathScenario(params)
            scenario.run()

    def tearDown(self) -> None:
        httpretty.disable()
        httpretty.reset()


if __name__ == "__main__":
    unittest.main()
