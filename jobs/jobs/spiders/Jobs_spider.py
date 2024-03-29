from scrapy import Spider, Request
from jobs.items import JobsItem
import re
import time
import urllib

class JobsSpider(Spider):
    name = 'jobs_spider'

    def start_requests(self):
        start_url = 'https://www.indeed.com/jobs'

        # 3 levels
        levels = ['entry', 'mid', 'senior']

        # 25 popular skills
        skills = ['java', 'python', 'r analytics', 'sql', 'hadoop', 'spark', 'c#', 'c++', 'javascript', 'angular', 'node.js', 'linux', 'tensorflow', 'kubernetes', 'docker', 'android', 'ios', 'aws', 'azure', 'kafka', 'vb', 'php', 'scala', 'golang', 'blockchain', 'elasticsearch']

        # 10 largest states
        states = ['California', 'Texas', 'Florida', 'New York', 'Illinois', 'Pennsylvania', 'Ohio', 'Georgia', 'North Carolina', 'Michigan']

        for level in levels:
            for skill in skills:
                for state in states:
                    url = start_url + '?q=' + urllib.parse.quote_plus(skill) + '&l=' + urllib.parse.quote_plus(state) + '&explvl=' + level + '_level&radious=100&limit=50'
                    meta = {'level': level, 'state': state, 'skill': skill}
                    yield Request(url=url, meta=meta, callback=self.parse)
                    
    def parse(self, response):
        total_jobs = response.xpath('//div[@id="searchCountPages"]/text()').extract()
        m = re.match(r'.+Page (\d+) of (\d+) jobs', total_jobs[0].replace(',', '').replace('\n', ''))
        total_jobs = int(m.group(2))

        # indeed have a limitation of 1000 jobs for paging
        if total_jobs > 1000:
            total_jobs = 1000
        
        total_pages = 1
        if total_jobs % 50 > 0:
            total_pages = total_jobs // 50 + 1
        else:
            total_pages = total_jobs // 50

        for i in range(0, total_pages):
            url_page = response.url + '&start=' + str(i * 50)
            yield Request(url=url_page, meta=response.meta, callback=self.parse_page)

    def parse_page(self, response):
        res = response.xpath('//div[contains(@class, "jobsearch-SerpJobCard unifiedRow row result")]')
        for i in range(1, len(res)):
            item = JobsItem()

            title = res[i].xpath('div[@class="title"]/a/text() | div[@class="title"]/a/b/text()').extract()
            item['title'] = ''.join(title).replace('\n','')

            company = res[i].xpath('div/div/span[@class="company"]/a/text() | div/div/span[@class="company"]/text()').extract()
            item['company'] = ''.join(company).replace('\n','')

            rating = res[i].xpath('div/div/span[@class="ratingsDisplay"]/a/span/text() | div/div/a/span[@class="ratings"]/@aria-label').extract()
            item['rating'] = ''.join(rating).replace('\n','').replace(' out of 5 star rating', '')
            
            location = res[i].xpath('div/div[contains(@class, "location")]/text() | div/span[contains(@class, "location")]/text()').extract()
            item['location'] = ''.join(location).replace('\n','')
            
            salary = res[i].xpath('div/span/span[@class="salaryText"]/text()').extract()
            salary = ''.join(salary).replace('\n','')
            if salary == '':
                continue

            if 'year' in salary:
                item['salary_unit'] = 'year'
                salary = salary.replace('a year', '')
            elif 'hour' in salary:
                item['salary_unit'] = 'hour'
                salary = salary.replace('an hour', '')
            elif 'month' in salary:
                item['salary_unit'] = 'month'
                salary = salary.replace('a month', '')
            elif 'week' in salary:
                item['salary_unit'] = 'week'
                salary = salary.replace('a week', '')
            elif 'day' in salary:
                item['salary_unit'] = 'day'
                salary = salary.replace('a day', '')
            else:
                print('Error Text: ' + salary)
                raise ValueError('Cannot parse salary text.')

            salary = salary.replace(',', '').replace(' ','').replace('$', '').replace('++', '').replace('From', '').replace('Upto', '')
            
            if '-' in salary:
                salary_all = salary.split('-')
                item['salary_from'] = salary_all[0]
                item['salary_to'] = salary_all[1]
            else:
                item['salary_from'] = salary
                item['salary_to'] = salary

            item['level'] = response.meta['level']
            item['state'] = response.meta['state']
            item['skill'] = response.meta['skill']

            yield item