# NHLSentimentRegression
Transformer based regression model, attempting to predict NHL player performance based off of sentiment of gameday tweets

Statistical data provided by Hockey Reference:
https://www.hockey-reference.com


The scrapers are currently functional. I suspect this is superfluous, however both scrapers take an extra descriptive argument. For example:

Using Alex Ovechkin as our example we can scrape his tweets using the following command: python twitter_user_scrape.y --handle ovi8
His stats can be scraped using the following: python player_stat_scrape.py --player o/ovechal01
