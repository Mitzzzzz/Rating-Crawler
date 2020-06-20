# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TestcrawlerItem(scrapy.Item):
    movieName = scrapy.Field()
    movieTitle = scrapy.Field()
    imdbRating = scrapy.Field()
    imdbPlotSummary = scrapy.Field()
    imdbURL = scrapy.Field()
    languages = scrapy.Field()
    Director = scrapy.Field()
    Cast = scrapy.Field()
    totalIMDBReviews = scrapy.Field()
    yearofRelease = scrapy.Field()
    lessthanorEqualtoFive = scrapy.Field()
    greaterthanFive = scrapy.Field()
    rottenTomatoesRating = scrapy.Field()
    genres = scrapy.Field()
    tomatometerScore = scrapy.Field()
    tomatoAudienceScore = scrapy.Field()
    tomatoCriticConsensus = scrapy.Field()


