#encoding=utf8
import scrapy
from livedata.items import LivedataItem
import json

class PandaTV(scrapy.Spider):

    name = 'pandaTV'

    allowed_domains = ['www.panda.tv']

    start_urls = ["https://www.panda.tv/all"]

    def parse(self, response):
        print(response.body)
        yield
