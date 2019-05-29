DROP DATABASE IF EXISTS exam2019;

CREATE DATABASE IF NOT EXISTS exam2019;

USE exam2019;

CREATE TABLE books (
  id INT AUTO_INCREMENT NOT NULL,
  fileName varchar(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  content LONGTEXT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE city (
  id INT AUTO_INCREMENT NOT NULL,
  name varchar(255) NOT NULL,
  geolocation GEOMETRY NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE city_mentions (
  city_id INT NOT NULL,
  book_id INT NOT NULL,
  foreign key (city_id) REFERENCES city(id),
  foreign key (book_id) REFERENCES books(id)
);

CREATE TABLE author (
  id INT AUTO_INCREMENT NOT NULL,
  name VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE book_authors (
  author_id INT NOT NULL,
  book_id INT NOT NULL,
  foreign key (author_id) REFERENCES author(id),
  foreign key (book_id) REFERENCES books(id)
);