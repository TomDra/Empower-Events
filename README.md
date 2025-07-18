COM2027, Group 19, Empower Events!
=====================================================

Running
----------------

### To run the project using docker:

Windows: execute `docker-compose up --build` in the root directory

Linux: execute `docker compose up --build` in the root directory


### To run the project without docker:

##### Install all the required packages:
- Console path = Group19/group19
- `pip install -r requirements.txt`
- `cd empower-events-app`
- `npm install`

#### To run the server you need 2 terminals/ consoles:
##### Console 1:
- Console path = Group19/group19
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py seed`
- `python manage.py runserver`

##### Console 2:
- Console path = Group19/group19/empower-events-app
- `npm start`


Login Information
----------------

#### Login information for regular user:
- Username: `john_doe`
- Password: `password123`

#### Login information for a charity:
- Charity Name: `Charity A`
- Password: `charityAPassword123`

Roles/ Specialitys
---------------

- Thomas - Full Stack
- Miles - Frontend
- Omar - Full Stack
- Mat - Backend
- Nishita - Frontend
- Yossef - Frontend
- Sam - Backend


