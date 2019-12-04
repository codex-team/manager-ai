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

    
    # database settings section (optional)
    database:
        # hostname or IP address of a MongoDB instance to connect to
        # see <https://api.mongodb.com/python/current/api/pymongo/mongo_client.html>
        host: "mongodb"

        # port of a MongoDB instance
        port: 27017

        # name of the database
        name: "manager"

    # proxy for performing tasks; tor proxy config
    proxy:
        # protocol of proxy
        protocol: "socks5"

        # host of proxy
        host: "localhost"

        # port of proxy
        port: 9050

        # username: "u53r14"

        # password: "p455w0rd88"
```
