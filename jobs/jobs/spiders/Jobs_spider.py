from scrapy import Spider
from jobs.items import JobsItem

class JobsSpider(Spider):
    name = 'jobs_spider'
    start_urls = ['https://www.indeed.com/jobs?q=java&l=CA&radius=100&limit=50&start=0']

    def parse(self, response):
        level = ['entry', 'mid', 'senior']

        res = response.xpath('//div[contains(@class, "jobsearch-SerpJobCard unifiedRow row result")]')
        for i in range(1, len(res)):
            item = JobsItem()

            title = res[i].xpath('div[@class="title"]/a/text() | div[@class="title"]/a/b/text()').extract()
            item['title'] = ''.join(title).replace('\n','')

            company = res[i].xpath('div/div/span[@class="company"]/a/text() | div/div/span[@class="company"]/text()').extract()
            item['company'] = ''.join(company).replace('\n','')
            
            #rating = res[i].xpath('div/div/a/span[@class="ratings"]/@aria-label').extract()
            rating = res[i].xpath('div/div/span[@class="ratingsDisplay"]/a/span/text()').extract()
            item['rating'] = ''.join(rating).replace('\n','')
            
            location = res[i].xpath('div/div[contains(@class, "location")]/text() | div/span[contains(@class, "location")]/text()').extract()
            item['location'] = ''.join(location).replace('\n','')
            
            salary = res[i].xpath('div/span/span[@class="salaryText"]/text()').extract()
            item['salary'] = ''.join(salary).replace('\n','')

            item['level'] = level[0]

            yield item