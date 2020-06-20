# -*- coding: utf-8 -*-
import scrapy

from ..items import TestcrawlerItem


class ImdbcrawlSpider(scrapy.Spider):
    name = 'imdbCrawl'  # should be unique name for each spider in a project
    ajax_url_review = None
    less_than_or_equaltoFive = 0
    greater_than_Five = 0
    allowed_domains = ["www.imdb.com"]
    current_parse = 0
    total_results = None
    review_count = 0
    max_limit = 1500
    parse_imdb_list = []

    def __init__(self, movieName='', **kwargs):
        self.start_urls = ['https://www.imdb.com/find?q=' + movieName + '&s=tt&exact=true&ref_=nv_sr_sm']  # py36
        super().__init__(**kwargs)  # python3

    def parse(self, response):
        items = TestcrawlerItem()
        ImdbcrawlSpider.total_results = None
        ImdbcrawlSpider.current_parse = 0
        if len(response.xpath('//a[@name="tt"]/../..').css('tr.findResult')) != 0:
            profile = response.xpath('//a[@name="tt"]/../..').css('tr.findResult')
            for pro in profile:
                item_title = pro.css('td.result_text a::text').get()
                movie_name = item_title
                item_title = item_title + pro.css('td.result_text::text').extract()[1]
                if 'TV Episode' not in item_title and 'Video' not in item_title and 'Short' not in item_title:
                    next_page = pro.css('td.result_text a::attr(href)').get()
                    obj = {"movieTitle": item_title, "pageURL": next_page, "movieName": movie_name,
                           "imdbURL": "https://www.imdb.com" + next_page}
                    print(obj)
                    ImdbcrawlSpider.parse_imdb_list.append(obj)
            ImdbcrawlSpider.total_results = len(ImdbcrawlSpider.parse_imdb_list)
            if ImdbcrawlSpider.total_results != 0:
                yield response.follow(ImdbcrawlSpider.parse_imdb_list[0]["pageURL"], callback=self.parseImdbDetail)

    def parseImdbDetail(self, response):
        print("Reached Imdb Parser")
        try:
            if ImdbcrawlSpider.current_parse < ImdbcrawlSpider.total_results and len(
                    response.css('div.ratingValue span[itemprop="ratingValue"]::text')) != 0:
                items = TestcrawlerItem()
                ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]['languages'] = []
                ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]['imdbRating'] = response.css(
                    'div.ratingValue span[itemprop="ratingValue"]::text').get()
                if len(response.xpath(
                        '//div[@class="credit_summary_item"]/h4[contains(text(),"Director")]/../a/text()')) != 0:
                    ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]['Director'] = response.xpath(
                        '//div[@class="credit_summary_item"]/h4[contains(text(),"Director")]/../a/text()').extract()
                elif len(response.xpath(
                        '//div[@class="credit_summary_item"]/h4[contains(text(),"Creator")]/../a/text()')) != 0:
                    ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]['Director'] = response.xpath(
                        '//div[@class="credit_summary_item"]/h4[contains(text(),"Creator")]/../a/text()').extract()
                ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]['Cast'] = response.xpath(
                    '//div[@class="credit_summary_item"]/h4[contains(text(),"Stars")]/../a/text()').extract()
                if "See full cast & crew" in ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]['Cast']:
                    ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]['Cast'].remove(
                        "See full cast & crew")
                ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]['yearofRelease'] = response.css(
                    'div.title_wrapper span#titleYear a::text').get()
                ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]['genres'] = []
                ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]['imdbPlotSummary'] = response.css(
                    '.plot_summary .summary_text::text').get().strip()
                for language in response.xpath(
                        '//div[@id="titleDetails"]/div[@class="txt-block"]/h4[contains(text(),"Language")]/../a/text()'):
                    ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]['languages'].append(
                        language.extract())
                for genre in response.css('div.title_wrapper a[href*="genres"]::text'):
                    ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]['genres'].append(genre.extract())
                reviews_string = response.css('div#titleUserReviewsTeaser a[href*="reviews"]::text').get()
                if reviews_string is not None:
                    if 'one' not in reviews_string:
                        number_of_reviews = [int(i.replace(',', '')) for i in reviews_string.split() if
                                             i.replace(',', '').isdigit()]
                        if number_of_reviews[0] > ImdbcrawlSpider.max_limit:
                            ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]['totalIMDBReviews'] = \
                                ImdbcrawlSpider.max_limit
                        else:
                            ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]['totalIMDBReviews'] = \
                            number_of_reviews[0]
                    else:
                        ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]['totalIMDBReviews'] = 1
                    reviews_page = response.css('div#titleUserReviewsTeaser a[href*="reviews"]::attr(href)').get()
                    yield response.follow(reviews_page, callback=self.parseReviews)
                else:
                    ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]['totalIMDBReviews'] = 0
                    for key in ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse].keys():
                        if key != "pageURL":
                            items[key] = ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse][key]
                    yield items
                    ImdbcrawlSpider.current_parse += 1
                    print("Parse Values are Current Parse " + str(
                        ImdbcrawlSpider.current_parse) + "and Total Results " + str(
                        ImdbcrawlSpider.total_results))
                    if ImdbcrawlSpider.current_parse < ImdbcrawlSpider.total_results:
                        yield response.follow(
                            ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]["pageURL"],
                            callback=self.parseImdbDetail)
            else:
                ImdbcrawlSpider.current_parse += 1
                print("Parse Values are Current Parse " + str(
                    ImdbcrawlSpider.current_parse) + "and Total Results " + str(
                    ImdbcrawlSpider.total_results))
                if ImdbcrawlSpider.current_parse < ImdbcrawlSpider.total_results:
                    yield response.follow(
                        ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]["pageURL"],
                        callback=self.parseImdbDetail)
        except Exception as e:
            print(e)

    def parseReviews(self, response):
        print("Reached Review Parser")
        items = TestcrawlerItem()
        if ImdbcrawlSpider.ajax_url_review is None:
            ImdbcrawlSpider.ajax_url_review = response.css('div.load-more-data::attr(data-ajaxurl)').extract()[0]
        for rating in response.css(
                'div.review-container span.rating-other-user-rating span:first-of-type::text').extract():
            if ImdbcrawlSpider.review_count < ImdbcrawlSpider.max_limit:
                ImdbcrawlSpider.review_count += 1
                if int(rating) <= 5:
                    ImdbcrawlSpider.less_than_or_equaltoFive += 1
                else:
                    ImdbcrawlSpider.greater_than_Five += 1
        if len(response.css('div.load-more-data::attr(data-key)')) != 0 and ImdbcrawlSpider.review_count < ImdbcrawlSpider.max_limit:
            pagination_key = response.css('div.load-more-data::attr(data-key)').extract()[0]
            next_page = 'http://www.imdb.com/' + ImdbcrawlSpider.ajax_url_review + '?paginationKey=' + pagination_key
            yield response.follow(next_page, callback=self.parseReviews)
        else:
            ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse][
                'lessthanorEqualtoFive'] = ImdbcrawlSpider.less_than_or_equaltoFive
            ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse][
                'greaterthanFive'] = ImdbcrawlSpider.greater_than_Five
            ImdbcrawlSpider.ajax_url_review = None
            for key in ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse].keys():
                if key != "pageURL":
                    items[key] = ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse][key]
            yield items
            ImdbcrawlSpider.less_than_or_equaltoFive = 0
            ImdbcrawlSpider.greater_than_Five = 0
            ImdbcrawlSpider.review_count = 0
            ImdbcrawlSpider.current_parse += 1
            print("Parse Values are Current Parse " + str(
                ImdbcrawlSpider.current_parse) + "and Total Results " + str(ImdbcrawlSpider.total_results))
            if ImdbcrawlSpider.current_parse < ImdbcrawlSpider.total_results:
                yield response.follow(ImdbcrawlSpider.parse_imdb_list[ImdbcrawlSpider.current_parse]["pageURL"],
                                      callback=self.parseImdbDetail)
