# database2019-exam
## Made By Tjalfe Moeller, Alexander Nielsen & David Carl
### Introduction

This exam assignment is the 'Gutenberg Project'. You can find it [here](https://github.com/datsoftlyngby/soft2019spring-databases/blob/master/Exam/GutenbergProject.md).

We used the provided download script from this [repository](https://github.com/datsoftlyngby/soft2018spring-databases-teaching-material/tree/master/book_download). The background to why we used this script is to make sure we dont hammer down their servers, but rather use the implemented sleep method in the script.

We decided to make this project in Python3 since it had most (if not all) of our desired features and all 3 of us is fairly competent in it.

### Databases

As for which 2 databases we decided on it is MongoDB and MySQL. We choose those 2 because first of we like JSON so MongoDB sounded like a good challange and we all was fairly confident in MySQL so it would be nice to see if we could match the 2 types of databases, or if we would have a hard time to do it.

#### MySQL

For our MySQL database we decided on a design that looks like this.

![MySQL ER](/images/ER-Diagram.png)

We chose to have 3 tables: books, authors and cities. The reason for this is because of the end-user queries where it would be easier to search a table for matches, then get the rest through the intermediate tables. 

#### Mongo

We decided to only use one collection for books, which look like this.
```js
Books : {
    _id : string,
    title : string,
    authors : [ string, ...],
    cities : { 
        city_name(string) : { 
            lat : float, 
            lng : float
        }, ...},
    file : string
}
```
The reason for this is, as a Mongo is file base database, we would like to keep it simple and use embedded documents. One of the key points that makes Mongo different from MySQL. 

As you can see, our city objects simply contain an latitude and longitude. That is *not* the correct way to store a geolocation in Mongo. The correct way is to use a GeoJSON object, which look like this:
```js
location : {
    type : "Point",
    coordinates : [float, float]
}
```
Unfortunately, we discovered this after we had made our api's and frontend. And we regrettably, found it too late. 


### Data handling

For our backend, we decided that we would use two Python libaries: `mysql` & `mongodb`. With these libaries, we made the database connectors and different queries.

We choose to send the data we got from the queries as JSON with api's. By doing that we could use JavaScript fetch calls to easily get the data to our frontend. One of the reasons for this approach was that we wished to send as little data as possible to clientside. Then we would use JavaScript to process the JSON into readable and well formatted HTML.

This of course, was easier with Mongo as it's already JSON objects. We only had to make some small mutations before we could send it to the frontend. With MySQL we had to completely re-format the data into JSON that we could send on. 

### Solutions to problems

The tasks we had is very focused on cities mentioned in books. Since all we got is books in text format we gotta figure out how to find the cities in the books. From here we got 2 possible ways to do it:

1. Get a dataset with cities and make regex to find it
1. Use the Standford Named Entity Recognizer (NER)

We decided to use solution 1, first and give ourself the posibility to use solution 2 later on if we got the time for it. We downloaded a dataset containing cities with a minimun amount of citizens of 5000. It can be found [here](download.geonames.org/export/dump/cities5000.zip).

We downloaded the zip file that contained a CSV file. One problem we found with this CSV file is that it was missing a header, so we would have a harder time than neccessary to retrieve information from this file. Luckily on the same page we downloaded the data we found something that could look like its header.
```
The main 'geoname' table has the following fields :
---------------------------------------------------
geonameid         : integer id of record in geonames database
name              : name of geographical point (utf8) varchar(200)
asciiname         : name of geographical point in plain ascii characters, varchar(200)
alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
latitude          : latitude in decimal degrees (wgs84)
longitude         : longitude in decimal degrees (wgs84)
feature class     : see http://www.geonames.org/export/codes.html, char(1)
feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
country code      : ISO-3166 2-letter country code, 2 characters
cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80) 
admin3 code       : code for third level administrative division, varchar(20)
admin4 code       : code for fourth level administrative division, varchar(20)
population        : bigint (8 byte int) 
elevation         : in meters, integer
dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
timezone          : the iana timezone id (see file timeZone.txt) varchar(40)
modification date : date of last modification in yyyy-MM-dd format
```
We made this command to fix it.
```
sed '1igeonameid\tname\tasciiname\talternatenames\tlatitude\tlongitude\tfeature_class\tfeature_code\tcountry_code\tcc2\tadmin1\tadmin2\tadmin3\tadmin4\tpopulation\televation\tdem\ttimezone\tmodification' cities5000.txt > correct.csv
```

### Import the data into the databases

Since this dataset is huge and it would have taken a long time to import it all into the databases row by row, we decided to process it all in Python. We constructed a bash grep command that made it possible to find a city in all the books fast, the quickets timing we recorded was 2 seconds to find if a city name had occured in all files and the slowest was around 25 seconds. We then made a python3 script that started a bash command for each city, and put the output in a file. We later used the information in this file to construct our table called 'city_mentions'. 

We also found out that its slower to make many insert statement and it much more optimisted to make a single multi insert, this cut out import time down by hours!

This made it to be a ton of SQL files that had to be executed to our MySQL database, we had over 22000 SQL files by the end of the project, and over 11 hours of runtime on a 20 threads (2 CPU's and 10 threads per CPU) and 80GB of ram. This was the reason for the quick runtime. We calculated this task to take around 7 days (168 hours) of constant compute time if we ran it on one of our laptops.

All of our data has been modified in one way or another in python before ever entering our MySQL database. For our MongoDB database, we simply choose to load data from our MySQL database and then importing it in our MongoDB. This was also done with Python3. What we did here was extract all ID's of books and then made a SQL statement that pulled out all relevant data on that book (author, cities mentioned etc.) and then format it to our MongoDB database format.

### End-user Queires

Some text about the 4 different end-user queries

### Conclusion

Our conclusion................

### Prerequisites
You will need a folder called unzipped stored in root of the project. This folder is supposed to hold the files you want to use. We used [these](dcarl.me/archive.tar), and then untarred them and unzipped the zipped files into the folder called unzipped.

Other than that you would also need to change the configuration in the configs folder. Here we have a MongoDB config and a MySQL config.

### How To Run

\#Todo: We have nothing note worthy to run yet!