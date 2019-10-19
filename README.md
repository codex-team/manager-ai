# Codex Manager bot

The main idea of this project is an increasing of projects performance inside of a little team. 

## Quick start
 1) create config/local_settings.py file and set or redefine_default configs in it
    ```python
    # sample config/local_settings.py
    PROXY = {"http": "socks5://127.0.0.1:9050", "https": "socks5://127.0.0.1:9050"}
    ```
 2) install requirements and start script or just launch the docker container

## About project structure

* tasks.py - entry point
* config.settings.py - public project settings
* config.local_settings.py - hidden project settings
* tmp - directory for logs and other temp files

## Default structure of file with tasks
```yaml
    tasks:
        # page that will be parsed
        \- url: 'https://t.me/s/codex_team'
        
        # xpath expression for watсhing element
        xpath: '/html/body/main/div/section/div[20]/div[1]/div[2]/div[3]/div/span[3]/a/time'
        
        # 7 days; number of seconds after which a notification will be sent if there were no changes
        max-secs-without-changes: 604800
        
        # url for sending notifications (see https://github.com/codex-bot/notify)
        notify-url: 'https://notify.bot.codex.so/u/'
        
        # string for scheduling in crontab-like syntax (see https://crontab.guru).
        schedule: '29 13-20 * * 1-5'
        
        # messages list to be send
        messages:
            'mess1'
            'mess2'
            'messN'
            
        # recipients only for this task
        recipients:
            'szzszdf'
            'asdfsd'
            'sdfsdfs'
```
