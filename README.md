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

- Thomas - Backend
- Miles - Frontend
- Omar - Full Stack
- Mat - Backend
- Nishita - Frontend
- Yossef - Frontend
- Sam - Backend


Getting started
---------------

Before you get started, you should update your com2027.yml file with your team members and project details. This will appear at [your static site](https://csee.pages.surrey.ac.uk/com2027/2023-24/Group19).

You have two branches created for you, `trunk` and `release`. The final commit on `release` will be marked.

Commits must be merged into `release` using a merge request, which requires two approvals. Force-pushing is disabled for both branches, as this can destroy your work. Only `trunk` can be merged into `release`.

You may develop directly on `trunk`, although it is recommended that you branch from `trunk` and submit merge requests (or merge directly onto the branch). How you use `trunk` is up to your team.

