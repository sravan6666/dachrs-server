Follow the below steps for running the flask application in local
Here we can run the application in two ways
    1. Using flask run
    2. Using Docker
======= Run the application using flask===========
1. Do the pip install for the root directory of the application using the below command
     pip install -r requirements.txt
2. After running the above command successfully then run the application using the below command
     flask run
3. If we get any errors while running the flask run then install the required libraries whatever shown in the flask run by using the below command
    pip install library-name
    EX: pip install flask

======== Run the application using Docker=============
1. build the project using the docker by using the below command
    docker image build .
2. get the port number using the below command in docker
    docker container ls
3. get the list of docker images running using the below command
    docker images
4. run the application using the below docker command
    docker run -p 5000 imageid(ex:a26c9e22babc)

======= DB Details ================
1. If we want to see the list of db tables available in mongo db use the below string value from the .flaskenv file under MONGO_CONNECTION_STR
<!-- mongodb://kanbandachrs:UfYcBuLcWSapeQi7PvakgneeWyOe6G1Hn4O8e4qiwLvI6czynHyOXCy75xlFNofAevNbbQ9MdheRKlPaMGXQow==@kanbandachrs.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@kanbandachrs@ -->
2. Connect the mongo db using mongo db compass or mongo client
3. if we use compass the copy paste the entire url there in the step1 and then click on connect.


flask run --> directly run the flask application
docker run -d --network=host -p 8055:8055  -v /home/ubuntu/:/home/ubuntu/ -e py_ms_demo:latest
server url :http://kanbandev.azurewebsites.net
