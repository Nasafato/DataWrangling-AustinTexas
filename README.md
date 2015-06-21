# DataWrangling-AustinTexas

My project is organized as follows:
* documents
  * Holds the project description, info.txt, and sources.txt files
* data
  * Holds the austin_sample.osm file
* cleaning
  * Holds the code I use to wrangle the data

## Using the driver

I do most of the work of running the cleaning code using my driver, which is in
*wrangler.py*. The only things I don't do from within the driver are importing the
JSON file into MongoDB and some simple MongoDB queries that I run inside the Mongo shell
instead.
