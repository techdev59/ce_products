
# Microservice Django app

It contains endpoints to manage products.

### Setup
1. take pull from git hub
2. install dependencies by using command:
```bash
pip install -r requirements.txt
```
3. create a .env file and put the database credentials in it.
4. to run the project:
```bash
python3 manage.py runserver
```

#### Note: 

if database doesn't contains any tables then you can create tables by using these commands (apply it after 3rd step):
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
