import scrapy
from web_scrapping_flipkart_mongodb.items import WebScrappingFlipkartMongodbItem


class FlipkartScrappingSpider(scrapy.Spider):
    name = 'flipkart_scrapping'
    id=1
    allowed_domains = ['flipkart.com']

    def start_requests(self):
        #providing the urls which we want to scrap
        urls = [
            'https://www.flipkart.com/clothing-and-accessories/topwear/pr?sid=clo%2Cash&otracker=categorytree&p%5B%5D=facets.ideal_for%255B%255D%3DMen&page={}',
            'https://www.flipkart.com/womens-footwear/pr?sid=osp%2Ciko&otracker=nmenu_sub_Women_0_Footwear&page={}']

        for url in urls:
            for i in range(1, 30):
                x = url.format(i)
                yield scrapy.Request(url=x, callback=self.parse)

    #Adding scraping logic for parsing.
    def parse(self, response):
        #finding all the similar properties using class name

        name = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "IRpwTa", " " ))]').xpath(
            'text()').getall()
        brand = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "_2WkVRV", " " ))]').xpath(
            'text()').getall()
        original_price = response.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "_3I9_wc", " " ))]').xpath('text()').getall()
        sale_price = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "_30jeq3", " " ))]').xpath(
            'text()').getall()
        image_url = response.css('._1a8UBa').css('::attr(src)').getall()
        product_page_url = response.css('._13oc-S > div').css('::attr(href)').getall()


         #Creating individual object from the group of products like extraction is giving list of items
        for i in range(0,len(name)):
            items = WebScrappingFlipkartMongodbItem()
            items['name'] = name[i]
            items['brand'] = brand[i]
            if(str(original_price[i])[1:].replace(",","")!=''):
                items['original_price'] = int(str(original_price[i])[1:].replace(",",""))
            else:
                items['original_price']=int(str(sale_price[i])[1:].replace(",",""))
            items['sale_price'] = int(str(sale_price[i])[1:].replace(",",""))
            items['image_url'] = str(image_url[i][1:])
            items['product_page_url'] = 'https://www.flipkart.com' + str(product_page_url[i])
            if 'women' in str(product_page_url).lower():
                items['product_category']='women footwear'
            elif 'men' in str(product_page_url).lower():
                items['product_category'] = 'men topwear'

            yield items
