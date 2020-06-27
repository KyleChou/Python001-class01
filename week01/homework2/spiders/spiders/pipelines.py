# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class SpidersPipeline:
    def process_item(self, item, spider):
        title = item['title']
        types = item['types']
        dates = item['dates']
        # output = f'|{title}|\t|{types}|\t|{dates}|\n\n'
        output = f'{title},{types},{dates}\n'
        with open('./movie.csv', 'a+', encoding='utf-8') as article:
            article.write(output)
        return item 