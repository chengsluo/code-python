from scrapy.spiders import CSVFeedSpider
from myproject.items import TestItem

class MySpider(CSVFeedSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/feed.csv']
    delimiter = ';'
    download_delay = 2
    quotechar = "'"
    headers = ['id', 'name', 'description']

    def parse_row(self, response, row):
        self.logger.info('Hi, this is a row!: %r', row)

        item = TestItem()
        item['id'] = row['id']
        item['name'] = row['name']
        item['description'] = row['description']
        return item

    # ---merge result!
    # def parse(self, response):
    # l = ItemLoader(item=Product(), response=response)
    # l.add_xpath('name', '//div[@class="product_name"]')
    # l.add_xpath('name', '//div[@class="product_title"]')
    # l.add_xpath('price', '//p[@id="price"]')
    # l.add_css('stock', 'p#stock]')
    # l.add_value('last_updated', 'today') # you can also use literal values
    # return l.load_item()