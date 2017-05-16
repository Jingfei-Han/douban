#encoding:utf-8
import scrapy
from douban.items import DoubanItem

class doubanSpider(scrapy.Spider):
	name = "douban"

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
	def start_requests(self):
		urls = [
			'http://movie.douban.com/top250'
		]

		for url in urls:
			yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

	def parse(self, response):
		for item_res in response.css("div.item"):
			item = DoubanItem()
			item1 = item_res.css("div.pic")
			item2 = item_res.css("div.info")

			item['index'] = int(item1.css("em::text").extract_first())
			item['title'] =  item2.css("span.title::text").extract_first()
			item['star'] = float(item2.css("span.rating_num::text").extract_first())
			info = item2.css("p::text").extract()[1].split('/')
			item['year'] = int(info[0].strip())
			item['country'] = info[1].strip()
			item['doubantype'] = info[2].strip()
			item['quote'] = item2.css("span.inq::text").extract_first()
			#print index, " ", title, " ",star, " ", year, " ", country, " ", type, " ", quote
			yield item
			

		#go to the next page
		next_page = response.css("span.next a::attr(href)").extract_first()

		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse)