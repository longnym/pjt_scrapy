# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JobsPipeline(object):
    def process_item(self, item, spider):
        print('Title: ' + item['title'])
        print('Company: ' + item['company'])
        print('Rating: ' + item['rating'])
        print('Location: ' + item['location'])
        print('Salary: ' + item['salary'])
        print('Level: ' + item['level'])
        print()
        return item
