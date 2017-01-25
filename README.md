# Search-Engine
Search Engine in Python


Note: This search engine is currently incomplete/not working 100%, but has enough code that you can view the following.

1). There is a scraper using the Scrapy framework. It currently uses BFS to scrape news pages off of the web.
2). There is an index file that indexes all of the pages and builds an inverted index for all of the words.
3). There is a file that computes Pagerank and a file that computes TF-IDF.
4). There is a file that runs the whole program in start.py and combines the TF-IDF and Pagerank scores
5). The cgi file can be ignored as it never worked. Will be replaced by some sort of Django interface later.


UPDATE 1/25: There is a new and improved crawler here https://github.com/benbrattain/Crawler/tree/master.
The goal of this crawler will be to run on a cluster and scrape articles (only new ones) from the WSJ, CNN, Fox News, and The Washington Post every day. The scraping is customized for each site in order to get better results. 

This Search Engine will be updated so it pulls from there and builds a new index on it's own on at least on a daily basis as well. The goal here is to have all of this run automatically every day so when a person runs the search engine, a lot less computational time is needed. Still a work in progress.

The current crawler in this file is no longer in use and will be removed once I get this search engine synced up with the new crawler that is linked above.
