import scrapy

from scrapy.loader import ItemLoader

from ..items import BankwestsdbankItem
from itemloaders.processors import TakeFirst


class BankwestsdbankSpider(scrapy.Spider):
	name = 'bankwestsdbank'
	start_urls = ['https://www.bankwest-sd.bank/about/news-alerts/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="co-community_impact--button"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="co-row co-full_width_text"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=BankwestsdbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
