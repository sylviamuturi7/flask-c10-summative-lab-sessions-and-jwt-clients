# My Journal API

This was my first big Flask project! I decided to go with session-based authentication 
instead of JWT because it seemed easier to manage user state. 

## What This Does

It's basically a digital journal app where users can:
- Sign up and log in securely 
- Create, read, update, and delete their own journal entries
- Only see their own stuff 

I used Flask-SQLAlchemy for the database and tried to keep things simple 
but functional. The pagination part was tricky.

## How to Get This Running

1. **Clone this repo**:
   ```bash
   git clone <repository-url>
   cd flask-c10-summative-lab-sessions-and-jwt-clients
   ```

2. **Install the requirements**:
   ```bash
   pip install -r requirements.txt
   ```
   
   i used Python 3.7+ 

3. **Set up the database**:
   ```bash
   flask db init
   flask db migrate -m "initial migration"
   flask db upgrade
   ```
   
   I made a simple setup script instead of using flask-migrate commands 
   because I kept messing up the migration files.

4. **Add some test data** (optional but recommended):
   ```bash
   python seed.py
   ```

## Running the App

```bash
flask run
```

The API will be running at `http://localhost:5000`

## API Endpoints I Built

### Authentication Stuff

| Method | Route | What it does |
|--------|-------|--------------|
| POST | /signup | Make a new user account |
| POST | /login | Log into your account  |
| GET | /check_session | See if you're still logged in |
| DELETE | /logout | Log out (clears session) 
 The signup route was tricky - make sure you send JSON 
or it will break

### Journal Entry Routes

| Method | Route | What it does |
|--------|-------|--------------|
| GET | /journal | Get all your journal entries |
| POST | /journal | Create a new journal entry |
| GET | /journal/\<id\> | Get one specific entry |
| PATCH | /journal/\<id\> | Update an existing entry |
| DELETE | /journal/\<id\> | Delete an entry |

**Warning:** The GET /journal/<id> route has a bug I haven't fixed yet - 
it doesn't check if the entry belongs to the logged-in user. 


## Test Users I Created

I made some test users so you don't have to create accounts every time:

| Username | Password |
|----------|----------|
| alice | password123 |
| bob | password456 |
| charlie | password789 |

Just run `python seed.py` to add them to your database. The database 
starts empty otherwise.


