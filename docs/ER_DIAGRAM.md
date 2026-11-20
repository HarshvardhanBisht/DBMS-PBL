# ER model (text representation)
- User 1:M Payment; each Payment refers to one Subscription_Plan.
- Genre 1:M Movie and Genre 1:M Series.
- Series 1:M Season; Season 1:M Episode.
- Actor 1:M Casting; each Casting points to exactly one Movie or Episode.
- User 1:M Review; each Review points to exactly one Movie, Series or Episode.
- User 1:M Watchlist; each Watchlist row points to exactly one Movie or Series.

The twelve core entities are User, Subscription_Plan, Payment, Movie, Series, Season,
Episode, Genre, Actor, Casting, Review and Watchlist. Dependent/associative entities
use their own surrogate IDs, avoiding nullable columns in composite primary keys.
