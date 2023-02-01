import re
import scrapy
from scrapy import Selector, Request
from seleniumwire import webdriver
from bs4 import BeautifulSoup

from movie.items import MovieItem


# 获取代理ip
def get_proxy():
    ip_browser_options = webdriver.ChromeOptions()
    ip_browser_options.add_argument("--headless")
    ip_browser = webdriver.Chrome(options=ip_browser_options)
    ip_browser.get("https://zj.v.api.aa1.cn/api/proxyip/?type=json")
    html_string = ip_browser.page_source
    ip_browser.close()
    # 正则表达式匹配
    match = re.search(r'ProxyIP":"(.*?)"', html_string)
    # 提取 IP:PORT
    if match:
        ip_port = match.group(1)
        return ip_port


# 爬虫本体
class MovieSpiderSpider(scrapy.Spider):
    name = 'movie_spider'
    allowed_domains = ['1080zyk3.com']

    # 设置网页url
    def start_requests(self):
        movie_type = getattr(self, 'movie_type', None)
        page = getattr(self, 'page', None)
        print(movie_type)
        print(page)
        if movie_type is not None and page is not None:
            yield scrapy.Request(url='https://1080zyk3.com/?m=vod-type-id-' + str(movie_type) + '-pg-' + page + '.html', callback=self.parse)
        else:
            pass

    def parse(self, response):
        response.meta['proxy'] = get_proxy()
        # 创建选择器
        sel = Selector(response)

        # 获取列表
        lis = sel.css('body > div.xing_vb > ul > li')

        # 遍历列表，提取影片元素
        for li in lis:
            link_tmp = li.css('span.xing_vb4 > a::attr("href")').extract_first()
            title_tmp = li.css('span.xing_vb4 > a::text').extract_first()
            if link_tmp is not None and title_tmp is not None:
                detail_link = 'https://1080zyk3.com/' + link_tmp
                movie_item = MovieItem()
                movie_item['detail_link'] = detail_link
                yield Request(
                    url=detail_link,
                    callback=self.parse_movie_link,
                    cb_kwargs={'item': movie_item}
                )

    def parse_movie_link(self, response, **kwargs):
        response.meta['proxy'] = get_proxy()
        movie_item = kwargs['item']
        sel = Selector(response)
        box = sel.css('body > div.warp > div:nth-child(1) > div > div')

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--proxy-server=' + get_proxy())
        chrome = webdriver.Chrome(options=chrome_options)
        chrome.get(movie_item['detail_link'])
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        chrome.close()
        lis = soup.select('body > div.warp > div:nth-child(4) > div.vodplayinfo > div > h3 > span > ul > li')
        links = []
        for li in lis:
            links.append(li.text)
        movie_item['title'] = box.css('div.vodInfo > div.vodh > h2::text').extract_first()
        movie_item['poster'] = box.css('div.vodImg > img::attr("src")').extract_first()
        movie_item['director'] = box.css('div.vodInfo > div.vodinfobox > ul > li:nth-child(2) > span::text').extract_first()
        movie_item['actor'] = box.css('div.vodInfo > div.vodinfobox > ul > li:nth-child(3) > span::text').extract_first()
        movie_item['type'] = box.css('div.vodInfo > div.vodinfobox > ul > li:nth-child(4) > span::text').extract_first()
        movie_item['area'] = box.css('div.vodInfo > div.vodinfobox > ul > li:nth-child(5) > span::text').extract_first()
        movie_item['released'] = box.css('div.vodInfo > div.vodinfobox > ul > li:nth-child(7) > span::text').extract_first()
        movie_item['links'] = links
        print(movie_item)
        yield movie_item











