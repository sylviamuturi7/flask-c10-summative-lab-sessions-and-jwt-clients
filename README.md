# Journal API

A Flask backend for a personal journaling app. Users can sign up, log in, and manage their own journal entries. No one else can see or touch your entries.

## What it does

This is a REST API that handles user authentication using sessions and lets each user create, read, update, and delete their own journal entries. Passwords are hashed so they're never stored in plain text, and every journal route checks that you're logged in before doing anything.

## Getting started

Clone the repo and navigate into it:

```bash
git clone <repository-url>
cd flask-c10-summative-lab-sessions-and-jwt-clients
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Set up the database:

```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

Seed it with some sample data:

```bash
python seed.py
```

## Running the app

```bash
flask run
```

The API will be running at `http://localhost:5000`

## Endpoints

### Auth

| Method | Route | What it does |
|--------|-------|--------------|
| POST | /signup | Create a new account |
| POST | /login | Log in |
| GET | /check_session | Check if you're still logged in |
| DELETE | /logout | Log out |

### Journal Entries

| Method | Route | What it does |
|--------|-------|--------------|
| GET | /journal | Get all your entries (paginated) |
| POST | /journal | Create a new entry |
| GET | /journal/\<id\> | Get one entry |
| PATCH | /journal/\<id\> | Update an entry |
| DELETE | /journal/\<id\> | Delete an entry |

For the journal index route you can pass `page` and `per_page` as query params, e.g. `/journal?page=2&per_page=5`. Defaults to page 1 with 10 entries per page.

## Test accounts

After seeding, you can log in with any of these:

| Username | Password |
|----------|----------|
| alice | password123 |
| bob | password456 |
| charlie | password789 |

