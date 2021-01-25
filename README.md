## Basic Api Car App
Adam Mańk

### Preface
App gives us the ability to save the model of a car &   
to add a rate from 1 to 5 to it.  
Car will be saved only if it exists in the external API.  
Listing saved cars by an amount of their rates also included. 

### Prerequisites
1. Docker
2. docker-compose
3. Linux os system

### Setup
Run those commands in the top directory (where docker files are).

To build & set up all the project:
>docker-compose up -d  

To make migrations & migrate:
>docker-compose exec web python app/manage.py makemigrations  
> 
>docker-compose exec web python app/manage.py migrate

To create a super user (admin):
>docker-compose exec web python app/manage.py createsuperuser

To shut down the app:
>docker-compose down

### Endpoints
    /cars       POST
    /cars       GET
    /popular    GET
    /rate       POST
JSON format!

### Tests
To run tests, simply use:
> docker-compose exec web python app/manage.py test

### Packages used
Described in the "requirements.txt"
1. Django==3.1.4
2. djangorestframework==3.12.2
3. psycopg2==2.8.6
4. requests==2.25.1

PostgreSQL used as a db.

### Deploy
You can check also this app on the given url:  
> https://basic-api-car-app.herokuapp.com/