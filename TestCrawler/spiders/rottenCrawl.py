# -*- coding: utf-8 -*-
import json
import sys

import scrapy

from ..tomato_items import TomatoCrawlerItem


class RottencrawlSpider(scrapy.Spider):
    name = 'rottenCrawl'  # should be unique name for each spider in a project
    allowed_domains = ["www.rottentomatoes.com"]
    current_parse = 0
    total_results = None
    review_count = 0
    max_limit = 1500
    parse_rotten_list = []

    def __init__(self, movieName='', **kwargs):
        self.start_urls = ['https://www.rottentomatoes.com/api/private/v2.0/search?q=' + movieName]  # py36
        super().__init__(**kwargs)  # python3

    def parse(self, response):
        RottencrawlSpider.total_results = None
        RottencrawlSpider.current_parse = 0
        result = json.loads(response.text)
        if len(result['movies']) != 0:
            for movie in result['movies']:
                obj = {"movieName": movie["name"], "pageURL": movie["url"], "yearofRelease": movie["year"],
                       "type": "Movie", "rottenURL": "https://www.rottentomatoes.com" + movie["url"]}
                RottencrawlSpider.parse_rotten_list.append(obj)
        if len(result['tvSeries']) != 0:
            for series in result['tvSeries']:
                obj = {"movieName": series["title"], "pageURL": series["url"], "yearofRelease": series["startYear"],
                       "type": "Series", "rottenURL": "https://www.rottentomatoes.com" + series["url"]}
                RottencrawlSpider.parse_rotten_list.append(obj)
        RottencrawlSpider.total_results = len(RottencrawlSpider.parse_rotten_list)
        if RottencrawlSpider.total_results != 0:
            yield response.follow(RottencrawlSpider.parse_rotten_list[0]["pageURL"], callback=self.parseRottenDetail)

    def parseRottenDetail(self, response):
        print("Reached Tomato Parser")
        try:
            if RottencrawlSpider.current_parse < RottencrawlSpider.total_results and len(response.css(
                    '.mop-ratings-wrap__row .mop-ratings-wrap__half .mop-ratings-wrap__percentage::text')) != 0:
                items = TomatoCrawlerItem()
                RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse]['tomatometerScore'] = response.css(
                    '.mop-ratings-wrap__row .mop-ratings-wrap__half .mop-ratings-wrap__percentage::text').get().strip()
                RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse][
                    'tomatoAudienceScore'] = response.css(
                    '.mop-ratings-wrap__row .mop-ratings-wrap__half.audience-score .mop-ratings-wrap__percentage::text').get().strip()
                RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse][
                    'tomatoCriticConsensus'] = response.css('p.mop-ratings-wrap__text--concensus::text').get()
                if RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse]["type"] == "Movie":
                    RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse]['Director'] = response.xpath(
                        "//ul[@class='content-meta info']/li[@class='meta-row clearfix']/div[contains(text(),'Directed By')]/../div[@class='meta-value']/a/text()").get()
                else:
                    RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse]['Director'] = response.xpath(
                        "//div[@class='tv-series__series-info-castCrew']/div/span[contains(text(),'Creator')]/../a/text()").get()
                reviews_page = response.css('div.mop-audience-reviews__view-all a[href*="reviews"]::attr(href)').get()
                if reviews_page is not None:
                    RottencrawlSpider.review_count = 0
                    RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse]["lessthanorEqualtoThree"] = 0
                    RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse]["greaterthanThree"] = 0
                    pattern = r'\broot.RottenTomatoes.context.fandangoData\s*=\s*(\{.*?\})\s*;\s*\n'
                    json_data = response.css('script::text').re_first(pattern)
                    RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse]["movie_id"] = \
                        json.loads(json_data)["emsId"]
                    next_page = "https://www.rottentomatoes.com/napi/movie/" + \
                                str(RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse][
                                        "movie_id"]) + "/reviews/user?direction=next&endCursor=&startCursor="
                    yield response.follow(next_page, callback=self.parseRottenReviews)
                else:
                    for key in RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse].keys():
                        if "pageURL" not in key and "type" not in key:
                            items[key] = RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse][key]
                    yield items
                    RottencrawlSpider.current_parse += 1
                    print("Parse Values are Current Parse " + str(
                        RottencrawlSpider.current_parse) + "and Total Results " + str(
                        RottencrawlSpider.total_results))
                    if RottencrawlSpider.current_parse < RottencrawlSpider.total_results:
                        yield response.follow(
                            RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse]["pageURL"],
                            callback=self.parseRottenDetail)
            else:
                RottencrawlSpider.current_parse += 1
                print("Parse Values are Current Parse " + str(
                    RottencrawlSpider.current_parse) + "and Total Results " + str(
                    RottencrawlSpider.total_results))
                if RottencrawlSpider.current_parse < RottencrawlSpider.total_results:
                    yield response.follow(
                        RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse]["pageURL"],
                        callback=self.parseRottenDetail)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(e)
            print(exc_tb.tb_lineno)

    def parseRottenReviews(self, response):
        print("Reached Rotten Review Parser")
        items = TomatoCrawlerItem()
        current_result = json.loads(response.text)
        for review in current_result["reviews"]:
            if RottencrawlSpider.review_count < RottencrawlSpider.max_limit:
                RottencrawlSpider.review_count += 1
                if review["score"] > 3:
                    RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse]["greaterthanThree"] += 1
                else:
                    RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse]["lessthanorEqualtoThree"] += 1
        if current_result["pageInfo"]["hasNextPage"] is True and RottencrawlSpider.review_count < RottencrawlSpider.max_limit:
            next_page = "https://www.rottentomatoes.com/napi/movie/" + \
                        str(RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse][
                                "movie_id"]) + "/reviews/user?direction=next&endCursor=" + str(
                current_result["pageInfo"][
                    "endCursor"]) + "&startCursor=" + str(current_result["pageInfo"]["startCursor"])
            yield response.follow(next_page, callback=self.parseRottenReviews)

        else:
            RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse][
                "totalRottenReviews"] = RottencrawlSpider.review_count
            for key in RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse].keys():
                if key != "pageURL" and key != "movie_id" and key != "type":
                    items[key] = RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse][key]
            yield items
            RottencrawlSpider.current_parse += 1
            print("Parse Values are Current Parse " + str(
                RottencrawlSpider.current_parse) + "and Total Results " + str(
                RottencrawlSpider.total_results))
            if RottencrawlSpider.current_parse < RottencrawlSpider.total_results:
                yield response.follow(
                    RottencrawlSpider.parse_rotten_list[RottencrawlSpider.current_parse]["pageURL"],
                    callback=self.parseRottenDetail)
