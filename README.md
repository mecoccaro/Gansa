# Gansa
This is an ongoing project for football pools, where you can join differents pools with your own predictions and you can monitor the results. It also has a side for the administrator of the pools, where you can enter results and manipulate users.

## Installation

Create a virtual environment.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```

After the package installation, create a database in [postgresql](https://www.postgresql.org/)

With your database credentials create `.env` for your variables:

```text
DB_NAME
DB_USER
DB_PASS
DB_HOST
DB_PORT
DEBUG 1/0
STAGE dev/prod
```

## Usage

Run all migrations for the database.

```bash
python manage.py migrate
```
Create a super user
```bash
python manage.py createsuperuser
```

Run the local django server
```bash
python manage.py runserver
```

## Contributors

https://github.com/mecoccaro
