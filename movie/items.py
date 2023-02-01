# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    detail_link = scrapy.Field()
    title = scrapy.Field()
    poster = scrapy.Field()
    director = scrapy.Field()
    actor = scrapy.Field()
    type = scrapy.Field()
    area = scrapy.Field()
    released = scrapy.Field()
    links = scrapy.Field()

