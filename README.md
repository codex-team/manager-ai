# Codex Manager bot

The main idea of this project is an increasing of projects performance inside of a little team. 

## Run in Docker
    1. Create file `config.docker.yml` with the content similar to `config.sample.yml`
    2. Change connection urls according to the Docker services (ex: ~~localhost:27017~~ `mongodb:27017`)
    3. Run `docker-compose up --build`
    
## Default structure of file with tasks
```yaml
      
    tasks:
      HelloWorld:
        # task name
        name: "Hello World"

        # string for scheduling in crontab-like syntax (see https://crontab.guru).
        schedule: "* * * * *" # minute, hour, day, month, day_of_week

        # scenario type
        scenario: "hello_world"

        # transport type
        transport: "stdout"
  
    TelegramPostChecker:
        # task name
        - name: "TelegramPostChecker"
        
        # string for scheduling in crontab-like syntax (see https://crontab.guru).
        schedule: "29 13-20 * * 1-5"
        
        # scenario type
        scenario: "xpath"
        
        # path to file with messages list to be send
        messages: "./messages.yml"
        
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

    
    # database settings section (optional)
    database:
        # hostname or IP address of a MongoDB instance to connect to
        # see <https://api.mongodb.com/python/current/api/pymongo/mongo_client.html>
        host: "mongodb"

        # port of a MongoDB instance
        port: 27017

        # name of the database
        name: "manager"
```