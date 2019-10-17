from scenarios.xpathscenario import XPathScenario

params_list = [
    # {
    #     'url': 'https://t.me/s/codex_team',
    #     'xpath': '/html/body/main/div/section/div[20]/div[1]/div[2]/div[3]/div/span[3]/a/time',
    #     'proxies': {
    #     }
    # },
    {
        'url': 'https://github.com/codex-team/manager-ai/pulls',
        'xpath': '//*[@id="issue_6"]/div/div[2]'
    },
    {
        'url': 'https://www.forbes.ru',
        'xpath': '//*[@id="top"]/div/div[1]/article'
    },
    {
        'url': 'https://yandex.ru',
        'xpath': '//*[@id="wd-_traffic"]/div/div[1]'
    }
]

print("Testing XPathScenario.run()...\n")

for params in params_list:
    my_scenario = XPathScenario(params)
    print(my_scenario.get_html_element_by_xpath())
    my_scenario.run()

print("\nCompleted. Checkout {XPathScenario.DEFAULT_TIMESTAMPS_FILE}")
