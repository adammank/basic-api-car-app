# Basic Api Car App
Adam Mańk

## Table of content:

1. App description
2. Endpoints & Allowed HTTP methods
3. Deploy
4. Setup via Docker
5. Setup via venv
6. Tests
7. Used Packages
___


### 1. App description
    App connects with the external APIand verifies, If the given
    car (make & model) exists in that source.
    If it exists, it will be saved in our PostgreSQL db.

    We can also add a rates to created car models.

    Cars will be listed regarding to its amount of added rates.

    App uses JSON as a primary format.


### 2. Endpoints & Allowed HTTP methods

    /cars/                  POST    Create a car in the db If it exists in the external api.
                                        {make:"make_name", model="model_name"} 

                            GET     Lists cars by amount of their rates.

                            HEAD, OPTIONS

    /cars/<car_model>/      GET, PUT, PATCH, DELETE, HEAD, OPTIONS


    /rates/                  POST    Add a rate to an existing model.
                                        {model:"model_name", rate=<int from 1 to 5>}

                            GET, HEAD, OPTIONS

    /rates/<rate_pk>        GET, PUT, PATCH, DELETE, HEAD, OPTIONS


### 3. Deploy
You can test this API app on the given urls:
> https://basic-api-car-app.herokuapp.com
>
> https://basic-api-car-app.herokuapp.com/cars
> 
> https://basic-api-car-app.herokuapp.com/rates


### 4. Setup via Docker
Prerequisites to set up project within the docker containers:
> Docker  
> docker-compose  
> Linux OS

Run those commands in the terminal in the top directory (where docker files are) for:

1. Build & set up all the project. Also, for further starting app:
   >docker-compose up -d

2. Make migrations & migrate:
    >docker-compose exec web python app/manage.py makemigrations  
    >
    >docker-compose exec web python app/manage.py migrate

3. Create a super user (admin):
    >docker-compose exec web python app/manage.py createsuperuser

4. To shut down the app:
    >docker-compose down


### 5. Setup via venv

Prerequisites to set up project with the virtual enviroment:
> Python == 3.8  
> Pipenv package for Python  
> PostgreSQL

Steps:
1. Create and start your PostgreSQL db
2. Change DATABASE section in config/settings.py module to match your criterias.
3. Run in the terminal in app top root directory (where Pipfile is) commands: 
   <p>&nbsp;</p>
   
    1*. Build & set up all the project:
   
   >    pipenv install
    
    2*. Make migrations & migrate:
   >    pipenv run python app/manage.py makemigrations  
   >    pipenv run python app/manage.py migrate
      
    3*. Start the server with:
      
    >   pipenv run python app/manage.py runserver


### 6. Tests
To run tests, simply use one of the underneath commands   
in the terminal of the top app root directory, depends on your project set up type:

> docker-compose exec web python app/manage.py test

> pipenv run python app/manage.py test


### 7. Used Packages
To see the full list of used packages in the project, go to the requirements.txt file.
