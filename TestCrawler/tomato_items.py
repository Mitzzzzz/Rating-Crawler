# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TomatoCrawlerItem(scrapy.Item):
    movieName = scrapy.Field()
    Director = scrapy.Field()
    totalRottenReviews = scrapy.Field()
    rottenURL = scrapy.Field()
    yearofRelease = scrapy.Field()
    lessthanorEqualtoThree= scrapy.Field()
    greaterthanThree = scrapy.Field()
    rottenTomatoesRating = scrapy.Field()
    tomatometerScore = scrapy.Field()
    tomatoAudienceScore = scrapy.Field()
    tomatoCriticConsensus = scrapy.Field()


