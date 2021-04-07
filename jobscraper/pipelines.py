# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobscraperPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy2003

    def process_item(self, item, spider):
        if 'hh' in item['source_name']:
            ready_salary = self.process_salary_hh(item['vacancy_salary'])
        elif 'superjob' in item['source_name']:
            ready_salary = self.process_salary_sj(item['vacancy_salary'])
        item['min_salary'] = ready_salary[0]
        item['max_salary'] = ready_salary[1]
        item['currency'] = ready_salary[2]
        del item['vacancy_salary']
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hh(self, vacancy_salary):
        if 'з/п не указана' in vacancy_salary:
            min_salary = 'з/п не указана'
            max_salary = 'з/п не указана'
            currency = 'з/п не указана'
            vacancy_salary = [min_salary, max_salary, currency]
        elif 'от ' in vacancy_salary and ' до ' not in vacancy_salary:
            min_salary = vacancy_salary[1].replace(u'\xa0', u' ')
            max_salary = 'з/п не указана'
            currency = vacancy_salary[3]
            vacancy_salary = [min_salary, max_salary, currency]
        elif 'до ' in vacancy_salary and 'от ' not in vacancy_salary:
            min_salary = 'з/п не указана'
            max_salary = vacancy_salary[1].replace(u'\xa0', u' ')
            currency = vacancy_salary[3]
            vacancy_salary = [min_salary, max_salary, currency]
        elif 'от ' in vacancy_salary and ' до ' in vacancy_salary:
            min_salary = vacancy_salary[1].replace(u'\xa0', u' ')
            max_salary = vacancy_salary[3].replace(u'\xa0', u' ')
            currency = vacancy_salary[5]
            vacancy_salary = [min_salary, max_salary, currency]
        return vacancy_salary
        pass

    def process_salary_sj(self, vacancy_salary):
        if 'По договорённости' in vacancy_salary:
            min_salary = 'По договорённости'
            max_salary = 'По договорённости'
            currency = 'По договорённости'
            vacancy_salary = [min_salary, max_salary, currency]
        elif 'от' in vacancy_salary and 'до' not in vacancy_salary:
            min_salary = vacancy_salary[2].replace(u'\xa0', u' ')
            max_salary = 'з/п не указана'
            currency = vacancy_salary[2][-4:]
            vacancy_salary = [min_salary, max_salary, currency]
        elif 'до' in vacancy_salary and 'от' not in vacancy_salary:
            min_salary = 'з/п не указана'
            max_salary = vacancy_salary[2].replace(u'\xa0', u' ')
            currency = vacancy_salary[2][-4:]
            vacancy_salary = [min_salary, max_salary, currency]
        elif 'от' not in vacancy_salary and 'до' not in vacancy_salary:
            min_salary = vacancy_salary[0].replace(u'\xa0', u' ')
            max_salary = vacancy_salary[4].replace(u'\xa0', u' ')
            currency = vacancy_salary[6]
            vacancy_salary = [min_salary, max_salary, currency]
        return vacancy_salary
        pass

