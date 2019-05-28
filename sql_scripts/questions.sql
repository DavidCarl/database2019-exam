# Question 1
# Given a city name your application returns all book titles with corresponding authors that mention this city.
SELECT c.name as CityName, b.id as bookID, b.fileName, b.title as BookTitle, a.name as AuthorName
FROM city c
INNER JOIN city_mentions cm on c.id = cm.city_id
INNER JOIN books b on cm.book_id = b.id
INNER JOIN book_authors ba on b.id = ba.book_id
INNER JOIN author a on ba.author_id = a.id
WHERE c.name = 'London';

# Question 2
# Given a book title, your application plots all cities mentioned in this book onto a map.
SELECT b.id as BookID, b.title as BookTitle, c.name as CityName, c.geolocation
FROM books b
INNER JOIN city_mentions cm on b.id = cm.book_id
INNER JOIN city c on cm.city_id = c.id
WHERE b.title = 'TestTitle';

# Question 3
# Given an author name your application lists all books written by that author and plots all cities mentioned in any of the books onto a map.
SELECT *
FROM author a
INNER JOIN book_authors ba on a.id = ba.author_id
INNER JOIN books b on ba.book_id = b.id
INNER JOIN city_mentions cm on b.id = cm.book_id
INNER JOIN city c on cm.city_id = c.id
WHERE a.name = 'HC Andersen'

# Question 4
# Given a geolocation, your application lists all books mentioning a city in vicinity of the given geolocation.
# TODO