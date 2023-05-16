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

ALTER TABLE users ADD COLUMN profile_image VARCHAR(255);
# alter table to use BLOB
ALTER TABLE users ALTER COLUMN profile_image TYPE bytea USING profile_image::bytea;

CREATE TABLE blogs(
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id)
);
```

```python
```

There are several ways to create and manage environments for a Flask application in Python. Here are three popular methods along with examples:

1. **Virtualenv**: Virtualenv is a tool for creating isolated Python environments. It allows you to have separate environments for different projects. Here's an example of creating a virtual environment for a Flask application using Virtualenv:

   ```plaintext
   # Create a new virtual environment
   python3 -m venv myenv

   # Activate the virtual environment
   source myenv/bin/activate
   
   0r myenv\Scripts\activate

   # Install Flask and other dependencies
   pip install flask

   # Run the Flask application
   flask run
   ```

2. **Pipenv**: Pipenv is a higher-level tool that combines virtual environment management with package dependency management. It simplifies the process of setting up and managing environments for your Flask application. Here's an example of using Pipenv for a Flask application:

   ```plaintext
   # Install Pipenv
   pip install pipenv

   # Create a new Pipenv environment and install Flask
   pipenv install flask

   # Activate the Pipenv shell
   pipenv shell

   # Run the Flask application
   flask run
   ```

3. **Conda**: Conda is a package and environment manager that can be used for Python development. It allows you to create separate environments with different Python versions and package configurations. Here's an example of using Conda for a Flask application:

   ```plaintext
   # Create a new Conda environment
   conda create --name myenv python=3.9

   # Activate the Conda environment
   conda activate myenv

   # Install Flask and other dependencies
   conda install flask

   # Run the Flask application
   flask run
   ```

These methods provide different approaches to creating and managing environments for your Flask application. Choose the one that best fits your needs and preferences.