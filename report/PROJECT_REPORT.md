# Movie Streaming & Subscription Platform — DBMS Project Report

## 1. Introduction
A relational database-backed catalogue for a movie and series subscription service.

## 2. Objectives
Design a relational database; manage users, subscriptions and payment records; represent
Series → Seasons → Episodes; manage genres, actors and casting; support reviews and
watchlists; and compare MySQL and PostgreSQL query behaviour.

## 3. Scope
Registration/login, catalogue browsing/search, watchlists, and simulated subscription
records. Video streaming and real payment processing are outside this prototype.

## 4. Entities
User, Subscription_Plan, Payment, Movie, Series, Season, Episode, Genre, Actor,
Casting, Review and Watchlist.

## 5. Relationships
Users can have multiple payments; each payment refers to one plan. Genres classify
movies and series. Series contain seasons; seasons contain episodes. Casting connects
actors to movies or episodes. Users save catalogue entries and submit reviews.

## 6. Normalization
Separate tables reduce repeated data. Primary and foreign keys define identity and
relationships. Independent surrogate IDs are used for dependent/associative records.
Atomic fields and separated entities support a design targeting 1NF, 2NF and 3NF.

## 7. Technology
Python, Flask, Flask-SQLAlchemy, HTML, CSS, MySQL and PostgreSQL. SQLite is used for
easy local setup before testing both required database systems.

## 8. Implementation
The Flask app provides registration, login, catalogue display/search, watchlists and
simulated plan selection. SQL scripts are supplied for both database engines.

## 9. Testing
Test account creation, duplicate email rejection, login, search, watchlist insertion,
plan selection and SQL queries. Compare the same query and dataset on both databases.

## 10. MySQL vs PostgreSQL
Run identical SELECT, JOIN, GROUP BY and EXISTS queries. Record execution time and
EXPLAIN output using the same data volume and indexes. Repeat tests; do not claim
one engine is faster without measurements.

## 11. Limitations
No video streaming, real payments, email verification, subscription expiry or
production-grade security.

## 12. Conclusion
The project demonstrates relational modelling and a web application based on a
streaming-service scenario, with a foundation for MySQL/PostgreSQL comparison.
