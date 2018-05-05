# -*- coding: utf-8 -*-
import re

import scrapy
from copy import deepcopy

from bole.items import BoleItem


class BlSpider(scrapy.Spider):
    name = 'bl'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        item = BoleItem()
        divs = response.xpath("//div[@class='post floated-thumb']")
        for div in divs:
            item['title'] = div.xpath(".//div[@class='post-thumb']/a/@title").extract_first()
            item['href'] = div.xpath(".//div[@class='post-thumb']/a/@href").extract_first()
            item["excerpt"] = div.xpath(".//div[@class='post-meta']//span/p/text()").extract_first()
            yield scrapy.Request(
                url=item["href"],
                callback=self.parse_detail,
                meta={'item':deepcopy(item)}
            )
        next_url = response.xpath("//a[@class='next page-numbers']/@href").extract_first()
        if next_url is not None:
            yield scrapy.Request(
                url=next_url,
                callback= self.parse
            )

    # 文章详情页的解析
    def parse_detail(self,response):
        item = response.meta['item']
        # item['publish_date'] =
        html = response.body.decode("utf-8")
        # item["title"] = response.xpath('//h3[@class="tb-main-title"]/text()').extract_first()
        date_pt = re.compile(r'<p class="entry-meta-hide-on-mobile">\s+(\d+/\d+/\d+)')
        item["date"] = date_pt.findall(html)[0]
        item['post_up'] = response.xpath("//h10/text()").extract_first()
        item['img_url'] = response.xpath("//div[@class='entry']/p/img/@src").extract()
        data = response.css("div.entry").extract_first()
        item['article'] = re.sub(r"</?.*?>|\s",'',data)
        yield item

