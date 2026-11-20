# How the project works
Flask receives browser requests and runs Python route functions. Flask-SQLAlchemy maps
Python classes to relational database tables. HTML templates render pages; CSS styles them.
Users can register, log in, browse/search catalogue entries, add movies or series to a
watchlist, and record a simulated subscription. Passwords are hashed. The app does not
collect payment-card details and does not charge money.

Start with SQLite locally. To use MySQL set DATABASE_URL to
mysql+pymysql://username:password@localhost/movie_streaming.
To use PostgreSQL set DATABASE_URL to
postgresql+psycopg2://username:password@localhost/movie_streaming.
Create the database first, then run seed.py and app.py.

Limitations: this academic prototype does not stream video, process real payments,
implement subscription expiry, or provide production-grade security.
