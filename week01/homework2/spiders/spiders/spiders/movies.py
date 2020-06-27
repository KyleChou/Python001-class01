# -*- coding: utf-8 -*-
import scrapy
from spiders.items import SpidersItem
# from bs4 import BeautifulSoup
from scrapy.selector import Selector


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/films?showType=3']

    def parse(self, response):
        # pass
        # print(response.url)
        # 打印网页的内容
        # print(response.text)
        movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]')
        # 取前10电影，初始化计数器
        movie_count = 0
        for movie in movies:
            # span 取class方法 [contains(@class,"name")]
            title = movie.xpath('.//span[contains(@class,"name")]/text()').extract_first()
            print('-----------')
            print(title)
            # print(title.extract())
            # print(title.extract_first())
            # print('-----------')

            hover_tags = movie.xpath('.//span[contains(@class,"hover-tag")]/../text()')
            # print('-----------')
            # print(hover_tags)
            # print(hover_tags[1])
            # print(hover_tags[5])
            # print(hover_tags.extract())
            # print((hover_tags.extract())[1].strip())
            # print((hover_tags.extract())[5].strip())
            types = (hover_tags.extract())[1].strip()
            dates = (hover_tags.extract())[5].strip()
            print(types)
            print(dates)
            print('-----------')

            item = SpidersItem()
            item['title'] = title
            item['types'] = types
            item['dates'] = dates
            yield item

            movie_count += 1
            if movie_count > 9:
                break

