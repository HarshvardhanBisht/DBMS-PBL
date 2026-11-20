-- All movies
SELECT * FROM movies;
-- Movies released after 2020
SELECT title, release_year FROM movies WHERE release_year > 2020;
-- Movie with genre
SELECT m.title,g.genre_name FROM movies m LEFT JOIN genres g ON m.genre_id=g.genre_id;
-- Count movies per genre
SELECT g.genre_name,COUNT(m.movie_id) AS movie_count FROM genres g LEFT JOIN movies m ON g.genre_id=m.genre_id GROUP BY g.genre_id,g.genre_name;
-- Users who have a payment (EXISTS)
SELECT u.full_name FROM users u WHERE EXISTS (SELECT 1 FROM payments p WHERE p.user_id=u.user_id);
-- Episodes with their series
SELECT s.title,se.season_number,e.episode_number,e.title FROM episodes e JOIN seasons se ON e.season_id=se.season_id JOIN series s ON se.series_id=s.series_id;
