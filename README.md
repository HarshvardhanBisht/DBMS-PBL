# CineVerse — Movie Streaming & Subscription Platform

## Requirements
Python 3.10+, VS Code recommended. SQLite is the easiest first run. MySQL Workbench
and PostgreSQL/pgAdmin are used later for the database comparison.

## First run (Windows)
1. Extract this ZIP and open the folder in VS Code.
2. Open Terminal in that folder.
3. Run `python -m venv venv`
4. Run `venv\\Scripts\\activate`
5. Run `pip install -r requirements.txt`
6. Run `python seed.py`
7. Run `python app.py`
8. Open `http://127.0.0.1:5000`

The default database is SQLite, so you can first see the website without configuring
MySQL or PostgreSQL.

## Database options
Set DATABASE_URL before starting the app:
- MySQL: `mysql+pymysql://username:password@localhost/movie_streaming`
- PostgreSQL: `postgresql+psycopg2://username:password@localhost/movie_streaming`

Create the database `movie_streaming` in the database server first. Use only one
DATABASE_URL at a time. Then run `python seed.py` and `python app.py`.

## Included
app.py (backend/models/routes), templates (pages), static (CSS), seed.py (demo data),
schema (MySQL and PostgreSQL DDL), sql (practice queries), docs (ER and explanation),
report (project report).

All plans and catalogue records are sample data. Subscription action is simulated;
no real payment is processed. This is a learning prototype, not a production OTT app.
