DROP DATABASE IF EXISTS exam2019;

CREATE DATABASE IF NOT EXISTS exam2019;

USE exam2019;

CREATE TABLE books (
  id INT AUTO_INCREMENT NOT NULL,
  fileName varchar(255) NOT NULL,
  title varchar(255) NOT NULL,
  author varchar(255),
  content LONGTEXT NOT NULL,
  PRIMARY KEY (id),
  FULLTEXT (content)
)