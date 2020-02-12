### To run application:
Build containers:  
```
docker-compose build
```
Run application:   
```
docker-compose up
```

### To check statuses of the tasks
Make sure that application is still running.   
Go to: http://0.0.0.0:8888/

### To test application
Make sure that application is running.   
On the other terminal run: 
```
docker-compose exec web py.test web/tests.py
```  

Application is based on:   
- Flask   
- MongoDB
- Celery
- Redis   
- Flower   
More in requirements.

#### What went good:  
- Factory patterns for celery, flask app
- Integration celery with flask
- Read/Writes from/to DB
- scalability of the project
- Virtualization of the project
##### What needs improvements/implementations:   
- Tests needs setUp tearDown functions
- Tests needs separate DB
- Downloading images needs links to DB