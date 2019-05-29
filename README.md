# database2019-exam
## Made By Tjalfe Møller, Alexander Nielsen & David Carl
## Group Name: Blin

## [Link to website](http://cloudless.guru:5000)

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

For our backend, we decided that we would use two Python libaries: `pymysql` & `pymongo`. With these libaries, we made the database connectors and different queries.

We choose to send the data we got from the queries as JSON with api's. By doing that we could use JavaScript fetch calls to easily get the data to our frontend. One of the reasons for this approach was that we wished to send as little data as possible to the client browser. Then we would use JavaScript to process the JSON into readable and well formatted HTML.

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

All of the following strings work for both MongoDB and MySQL. We tried our best to have a 1 to 1 database.

 http://cloudless.guru:5000/search_city

 You can search by the following strings, its a mix of bigger and smaller cities. This should give a mixed result set: ``` Copenhagen | London | Washington | Ordino | Kukes ``` 

 http://cloudless.guru:5000/search_title

 You can search by the following strings: ``` Beauty and the Beast, | The Valley of Vision, | Shakspere & Typography, | The Boy Ranchers, | Irma in Italy, ```

 http://cloudless.guru:5000/search_author
 
 You can search by the following strings: ``` Noel Coward | Frank E. Miller | Mary E. Wilkins Freeman | W.W. Jacobs | Rex Beach ```

 http://cloudless.guru:5000/search_location
 
 You can search the following lat lng pairs, they are seperated : ``` 55.76243279434027:12.49851688755325 | 55.676574443752095:12.54795536411575 | 52.44471802074383:13.347558151491285 | 53.48045301989892:-2.2849070613417553 | 35.76761261754951:-78.66225517099298 ```

Since we failed in building up a proper MongoDB these queries will not work if you select MongoDB instead of MySQL.

Here we recommand you to play around a bit with the map and click on it for some time since its interactive and fun to play with. It is still required to click the `Search` button, for results.

#### Timings

**Search_city**

| Query String 	| MySQL   	| MongoDB 	|
|--------------	|---------	|---------	|
| Copenhagen   	| 3125ms  	| 46ms    	|
| London       	| 3351ms  	| 151ms   	|
| Washington   	| 3179ms  	| 80ms    	|
| Ordino       	| 27ms    	| 57ms    	|
| Kukes        	| 3051ms 	| 43ms    	|

**Search_title**

| Query String            	| MySQL 	| MongoDB 	|
|-------------------------	|-------	|---------	|
| Beauty and the Beast,   	| 41ms  	| 18ms    	|
| The Valley of Vision,   	| 38ms  	| 19ms    	|
| Shakspere & Typography, 	| 27ms  	| 19ms    	|
| The Boy Ranchers,       	| 30ms  	| 18ms    	|
| Irma in Italy,          	| 39ms  	| 18ms    	|

Its important to keep all the commas as we failed our data cleanup a bit, and failed to remove these. So if its not in the name it will not be possible to find the books.

**Search_Author**

| Query String            	| MySQL 	| MongoDB 	|
|-------------------------	|-------	|---------	|
| Noel Coward             	| 62ms  	| 25ms    	|
| Frank E. Miller         	| 49ms  	| 27ms    	|
| Mary E. Wilkins Freeman 	| 101ms 	| 33ms    	|
| W.W. Jacobs             	| 141ms 	| 37ms    	|
| Rex Beach               	| 92ms  	| 37ms    	|

**Search_location**

| Query String                          	| MySQL 	| MongoDB 	|
|---------------------------------------	|-------	|---------	|
| 55.76243279434027:12.49851688755325   	| 2518ms  	|   N/A	    |
| 55.676574443752095:12.54795536411575  	| 2558ms  	|   N/A 	|
| 52.44471802074383:13.347558151491285  	| 2526ms  	|   N/A 	|
| 53.48045301989892:-2.2849070613417553 	| 2830ms   	|   N/A 	|
| 35.76761261754951:-78.66225517099298  	| 2475ms  	|   N/A 	|

### Conclusion

As you have read above, Mongo is faster MySQL for this kind of project. But it's hard for us to pick one above the other. We have a deeper knowledge of MySQL so we found it easier to work with, which allowed us to work faster with MySQL than Mongo. We also did not complete query 4 for Mongo due to our lack of knowlegde. 

Due to the way we decided to set up our api to use JSON, Mongo also has a clear advantage over MySQL. 

But we feel it's more straightforward to get the data out of MySQL, with a few inner join we could effordlessly get exactly what we wanted. We also like that there are concrete rules for what data is where in an ER database. 

For a MySQL improvement, we should index our titles and authors to make it faster to search for them. As most (if not all) important fields are indexed which makes it faster to search. Otherwise we mainly use ID's (primary keys) which by default are indexed.

In the end, if we look past our own bias, we would probably recommend Mongo as the most effecient database for this exerice. It's in most cases faster than MySQL and with proper expertise you would perhaps not run into some of the problems that we had with Mongo. 
