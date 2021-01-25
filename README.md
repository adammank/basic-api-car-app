## Basic Api Car App
Adam Mańk

### Preface
App gives us the ability to save the model of a car &   
to add a rate from 1 to 5 to it.  
Car will be saved only if it exists in the external API.  
Listing saved cars by an amount of their rates also included. 

### Deploy
You can use this app on the given urls:  
> https://basic-api-car-app.herokuapp.com/cars  

> https://basic-api-car-app.herokuapp.com/popular  

> https://basic-api-car-app.herokuapp.com/rate

### Endpoints
    /cars       POST    Add a car if it exists in the external api.
                        {make:"make_name", model="model_name"} 

    /cars       GET     Lists cars with their average rate.

    /popular    GET     Lists cars by amount of their rates.

    /rate       POST    Add a rate to an existing model.
                        {model:"model_name", rate=<from 1 to 5>}

### Prerequisites for setting it locally
1. Docker
2. docker-compose
3. Linux os system

### Setup
Run those commands in the top directory (where docker files are).

To build & set up all the project:
>docker-compose up -d  

To make migrations & migrate:
>docker-compose exec web python app/manage.py makemigrations  

>docker-compose exec web python app/manage.py migrate

To create a super user (admin):
>docker-compose exec web python app/manage.py createsuperuser

To shut down the app:
>docker-compose down

### Tests
To run tests, simply use:
> docker-compose exec web python app/manage.py test

### Packages used
Described in the "requirements.txt"
1. Django==3.1.4
2. djangorestframework==3.12.2
3. psycopg2==2.8.6
4. requests==2.25.1

PostgreSQL as a db.  
JSON as a primary format.