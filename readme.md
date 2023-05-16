### setup
##### Create virtual envrionmentcls
if you are using virtualenv by default comes in pycharm
- Create virtual env : py -m venv .
- cd Scripts
- activate
- Deactivate by running: deactivate


#### Using pipenv
check if you have pipenv : pipenv --version
- pipenv shell
- pipenv install flask flask-jwt-extended psycopg2 psycopg2-binary flask-sqlachemy python-dotenv gunicorn
- flask run or python app.py


```SQL
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)
```