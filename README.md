# studentTest

<p align="center">
  <img src ="https://storage.caktusgroup.com/media/blog-images/drf-logo2.png" />
</p>


This API was created to make two POST type requests

- '/login/' : returns a token if the user exists
- '/answer/' : records user responses

## Clone the repository

```bash
https://github.com/Danielmc09/studentTest.git
```
## Create virtual env and activate 

```bash
create:
  virtualenv name_env 
  
activate:
  On Unix or MacOS, using the bash shell: source venv/bin/activate
  On Windows using the Command Prompt: path\venv\Scripts\activate.bat
```
## Install libraries

```bash
pip install -r requirements.txt
```

## Run proyect

```bash
python manage.py runserver
```

## Create migrations

```bash
- python manage.py makemigration
- python manage.py migrate
```

## Create super user

#### - To create test data, you can create a super user and via django admin register some data

```bash
- python .\manage.py createsuperuser
```

## Run Test

```bash
Inside the project at the manage.py file run the following commands

- coverage run --source='studentTest' manage.py test
- coverage html

the first command runs the Tests declared in the tests file, the second command displays the coverage
```


## General notes 

- The database used in this project is sqlite3

- Ports to use that should not be busy or with local services turned off:
  - Django: 8000

|Path|Verb|
|----|----|
|Local|
|http://localhost:8000/admin/||
|http://localhost:8000/login/|POST|
|http://localhost:8000/answer/|POST|


# studentTest test online

|Path|Verb|
|----|----|
|Deploy railway|
|https://studenttest-production-6a84.up.railway.app/admin/|POST|
|https://studenttest-production-6a84.up.railway.app/login/|POST|
|https://studenttest-production-6a84.up.railway.app/answer/|POST|

## Data to take into account

```bash
- user: admin
- pass: admin123
```

## Collection postman online 

```bash
the postman collection has an example with a user already created in the database and some questions

https://www.postman.com/restless-comet-941245/workspace/studenttest/request/11211559-09a42840-7a14-44be-8a05-9253698f9602

```


Autor: <a href="https://www.linkedin.com/in/angeldanielmendieta/">Angel Daniel Menideta Castillo</a> © 2023
