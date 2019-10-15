# Codex Manager bot

The main idea of this project is an increasing of projects performance inside of a little team. 
 
## Quick start
 
1. Clone repo & create virtual environment & install dependencies

       ~/path/to$ git clone https://github.com/SunnyCapt/manager-ai.git && cd manager-ai 
       ~/path/to/manager-ai$ sudo pip3 install virtualenv
       ~/path/to/manager-ai$ virtualenv venv
       ~/path/to/manager-ai$ source venv/bin/activate
       ~/path/to/manager-ai$ pip install -r requirements.txt
       ~/path/to/manager-ai$ pip install -r requirements.txt
       ~/path/to/manager-ai$ apt-get install redis-server -y
       ~/path/to/manager-ai$ sudo systemctl enable redis
       
2. Launch tasks
    
       ~/path/to/manager-ai$ celery -A tasks worker -l info
       ~/path/to/manager-ai$ celery -A tasks beat -l info
       
## About project structure

* tasks.py - main script. It starts checking and notifying.
* services.py - application logic
* settings.py - public project settings
* local_settings.py - hidden project settings

## Default structure of file with tasks

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
        recipients: ['szzszdf', 'asdfsd', 'sdfsdfs']