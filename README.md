# Gansa
This is an ongoing project for football pools, where you can join different pools with your own predictions and monitor the results. It also includes an admin side where administrators can enter results and manage users.## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Additional Information](#additional-information)
- [Contributors](#contributors)
## Installation
### Step 1: Clone the Repository
First, clone the repository to your local machine.
```bash
git clone https://github.com/yourusername/gansa.git
cd gansa
```
### Step 2: Create a Virtual Environment
Create a virtual environment to manage dependencies. You can use `venv`:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### Step 3: Install Requirements
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.
```bash
pip install -r requirements.txt
```
### Step 4: Create a PostgreSQL Database
Create a database in [PostgreSQL](https://www.postgresql.org/). You can do this using `psql`:
```sql
CREATE DATABASE gansa;
CREATE USER gansa_user WITH PASSWORD 'yourpassword';
ALTER ROLE gansa_user SET client_encoding TO 'utf8';
ALTER ROLE gansa_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE gansa_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE gansa TO gansa_user;
```
### Step 5: Configure Environment Variables
Create a `.env` file in the root directory of the project and add your database credentials and other variables:
```text
DB_NAME=gansa
DB_USER=gansa_user
DB_PASS=yourpassword
DB_HOST=localhost
DB_PORT=5432
DEBUG=1  # Use 0 for production
STAGE=dev  # Use prod for production
```
## Usage
### Step 1: Apply Database Migrations
Run all migrations to set up the database schema.
```bash
python manage.py migrate
```
### Step 2: Create a Superuser
Create a superuser to access the Django admin interface.
```bash
python manage.py createsuperuser
```
### Step 3: Run the Development Server
Run the local Django server.
```bash
python manage.py runserver
```
## Additional Information
### Hardcoded Tournament ID
The current tournament ID is hardcoded in the project. You might need to update this manually based on your needs.
### Main Logic for Games
The majority of the game logic can be found in the `gameInput.html` file. Make sure to review this file for any specific game-related logic and updates.
## Contributors
- [mecoccaro](https://github.com/mecoccaro)
- [jrcapriles](https://github.com/jrcapriles)