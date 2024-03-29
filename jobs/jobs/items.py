# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class JobsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    company = scrapy.Field()
    rating = scrapy.Field()
    location = scrapy.Field()
    salary_unit = scrapy.Field()
    salary_from = scrapy.Field()
    salary_to = scrapy.Field()
    level = scrapy.Field()
    state = scrapy.Field()
    skill = scrapy.Field()