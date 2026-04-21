# My Journal API

This was my first big Flask project! I decided to go with session-based authentication 
instead of JWT because it seemed easier to manage user state. Took me forever 
to figure out how to properly hash passwords with Flask-Bcrypt lol.

## What This Thing Does

It's basically a digital journal app where users can:
- Sign up and log in securely (passwords are hashed!)
- Create, read, update, and delete their own journal entries
- Only see their own stuff (no peeking at other people's journals)

I used Flask-SQLAlchemy for the database and tried to keep things simple 
but functional. The pagination part was tricky - had to read the docs 
like 5 times to get it right.

## How to Get This Running

1. **Clone this repo** (if you haven't alrea:
   ```bash
   git clone <repository-url>
   cd flask-c10-summative-lab-sessions-and-jwt-clients
   ```

2. **Install the requirements**:
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note:** Make sure you're using Python 3.7+ or you'll get weird errors.

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
| DELETE | /logout | Log out (clears session) |

**Quick tip:** The signup route was tricky - make sure you send JSON 
or it will break! I learned that the hard way.

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
Whoops!


## Test Users I Created

I made some test users so you don't have to create accounts every time:

| Username | Password |
|----------|----------|
| alice | password123 |
| bob | password456 |
| charlie | password789 |

Just run `python seed.py` to add them to your database. The database 
starts empty otherwise, which is annoying for testing.

**Fun fact:** I used simple passwords because I kept forgetting 
the test ones while debugging. Don't judge lol.

