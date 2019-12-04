# Codex Manager bot

The main idea of this project is an increasing of projects performance inside of a little team. 

## Quick start
 1) create config/local_settings.py file (check config/local_settings.sample) and set or redefine_default configs in it
 2) install requirements and start script or just launch the docker container

## About project structure

* tasks.py - entry point
* config.settings.py - public project settings
* config.local_settings.py - hidden project settings
* tmp - directory for logs and other temp files

## Default structure of file with tasks
```yaml
      
    tasks:
        # task name
        - name: "Check last telegram post date"
        
        # string for scheduling in crontab-like syntax (see https://crontab.guru).
        schedule: "29 13-20 * * 1-5"
        
        # scenario type
        scenario: "xpath"
        
        # path to file wuth messages list to be send
        messages: messages.sample.yml
        
        # page that will be parsed
        url: "https://t.me/s/codex_team"
        
        # xpath expression for watсhing element
        xpath: "/html/body/main/div/section/div[20]/div[1]/div[2]/div[3]/div/span[3]/a/time"
        
        hooks:
        
          # on_changed action
          changed:
            notifier: "Telegram"
            
          # on_no-changed action  
          no-changes:
            notifier: "Work Email"
            time: 40000

    notifiers:
        - name: "Telegram"
        type: "telegram"
        webhook: "https://notify.bot.codex.so/u/R4ND0M"
        - name: "Work Email"
        type: "email"
        address: "work@me.ru"
```
