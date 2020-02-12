###To run application:
Build containers:  
```
docker-compose build
```
Run application:   
```
docker-compose up
```

###To test application
Make sure that application is running.   
On the other terminal run: 
```
docker-compose exec web py.test web/tests.py
```  
	