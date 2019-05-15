# database2019-exam
## Made By Tjalfe Moeller, Alexander Nielsen & David Carl
### Introduction

This exam assignment is the 'Gutenberg Project'. You can find it [here](https://github.com/datsoftlyngby/soft2019spring-databases/blob/master/Exam/GutenbergProject.md).

We used the provided download script from this [repository](https://github.com/datsoftlyngby/soft2018spring-databases-teaching-material/tree/master/book_download). The background to why we used this script is to make sure we dont hammer down their servers, but rather use the implemented sleep method in the script.

We decided to make this project in Python3 since it had most (if not all) of our desired features and all 3 of us is fairly competent in it.

As for which 2 databases we decided on it is MongoDB and MySQL. We choose those 2 because first of we like JSON so MongoDB sounded like a good challange and we all was fairly confident in MySQL so it would be nice to see if we could match the 2 types of databases, or if we would have a hard time to do it.

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
### How To Run

\#Todo: We have nothing note worthy to run yet!