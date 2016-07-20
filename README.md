# scramble
Sample implementation of web scraping.

## Use Case
#### This system is designed to:
1. periodically retrieve data from the news website, theguardian.com
2. make that data available via a REST api

#### For each article found, this system stores:
1. url
2. headline
3. author
4. text

## Components
```
                        Scramble
                            |
                            |
             --------------------------------
            |                                |
            |                                |
       Web Scraper                      Search API
        (Scrapy)                         (PyMongo)
        (PyMongo)                            |
            |                                |
            |                                |
             --------------------------------
                            |
                            |
                        Article DB
                        (Mongo DB)
```

## Web Scraper
### Build and Test
```
$> cd scramble
$> pip install -r requirements.txt
$> cd icicle
$> scrapy check
```

### Deploy
1. Add entry to crontab to invoke this code every 5 hours 
```
$> cd scramble/icicle
$> scrapy crawl guardian-icicles
```

## API
### Test
1. Dev version can be accessed at https://9u56icss4c.execute-api.us-west-2.amazonaws.com/dev/search/b64_encoded_search_string
2. Search string must be b64 encoded to allow appending as a query string
3. To test functionality, call the python file directly via the command line
```
$> python scramble/api/src/search/search_text.py "what you are looking for"
```
4. To test the hosted API setup, use the sample_search tool
```
$> python scramble/api/test/sample_search.py "what you are looking for"
```

### Deploy
```
$> cd scramble/api/src/search

# assuming awscli is installed in your system
$> ../../ci/deploy_lambda.sh
```

## Credits
1. https://realpython.com/blog/python/web-scraping-with-scrapy-and-mongodb/
    - for getting me started really quick