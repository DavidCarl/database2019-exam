-- # Question 1
-- # Given a city name your application returns all book titles with corresponding authors that mention this city.
SELECT c.name as CityName, b.id as bookID, b.fileName, b.title as BookTitle, a.name as AuthorName
FROM city c
INNER JOIN city_mentions cm on c.id = cm.city_id
INNER JOIN books b on cm.book_id = b.id
INNER JOIN book_authors ba on b.id = ba.book_id
INNER JOIN author a on ba.author_id = a.id
WHERE c.name = 'London';

-- # Question 2
-- # Given a book title, your application plots all cities mentioned in this book onto a map.
SELECT b.id as BookID, b.title as BookTitle, c.name as CityName, ST_Latitude(geolocation) as Latitude, ST_Longitude(geolocation) as Longitude
FROM books b
INNER JOIN city_mentions cm on b.id = cm.book_id
INNER JOIN city c on cm.city_id = c.id
WHERE b.title = 'Legends of Saints & Sinners,';

-- # Question 3
-- # Given an author name your application lists all books written by that author and plots all cities mentioned in any of the books onto a map.
SELECT a.name, b.title, c.name, ST_Latitude(c.geolocation) as Latitude, ST_Longitude(c.geolocation) as Longitude
FROM author a
INNER JOIN book_authors ba on a.id = ba.author_id
INNER JOIN books b on ba.book_id = b.id
INNER JOIN city_mentions cm on b.id = cm.book_id
INNER JOIN city c on cm.city_id = c.id
WHERE a.name = 'Mor Jokai';

-- # Question 4
-- # Given a geolocation, your application lists all books mentioning a city in vicinity of the given geolocation.
-- # Part 1 - This returns IDs of all the cities in the vicinity
WITH vicinity as (select ST_GeomFromText(ST_ASTEXT(ST_Buffer(ST_GeomFromText("POINT (42.50720 1.53410)", 0), 0.1)), 4326) as area)
SELECT city.name, city.id
FROM vicinity, city
WHERE ST_WITHIN(city.geolocation, vicinity.area);
-- # Part 2 - Here we need to make a list of the returned IDs and put them in here
SELECT b.id, b.title, c.name
FROM books b
INNER JOIN city_mentions cm ON b.id = cm.book_id
INNER JOIN city c ON cm.city_id = c.id
WHERE c.id IN (1,2,3,4,5,6) AND b.title != '';