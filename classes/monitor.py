# coding = utf-8

import requests

import threading
import re
import json
from time import sleep

from logger import Logger
from product import Product

L = Logger()
log = L.log


class Monitor(threading.Thread):
    def __init__(self, site_url, proxy=None):
        threading.Thread.__init__(self)
        self.s = requests.Session()
        self.site_url = site_url
        L.name = site_url
        self.products = []
        self.s.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
                          'e/61.0.3163.100 Safari/537.36'
        }
        self.s.verify = 'charles-ssl-proxying-certificate.pem'
        self.proxy = proxy
        if self.proxy is not None:
            self.s.proxies.update({
                'http':  'http://{}'.format(self.proxy),
                'https': 'https://{}'.format(self.proxy)
            })
        with open('./config.json') as config:
            self.config = json.load(config)
        with open('./keywords.json') as keywords:
            self.keywords = json.load(keywords)

    def scrape_products(self):
        log('scraping products')
        r = self.s.get(
            '{}/sitemap_products_1.xml'.format(self.site_url)
        )
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            log('error {} on sitemap request'.format(r.status_code))

        expression = '<loc>(.*)</loc>\s.*</lastmod>\s.*\s.*\s.*\s.*\s.*\s.*<image:title>(.*)</image:title>'
        products = re.findall(expression, r.text)
        product_objects = []
        for prod in products:
            product_objects.append(Product(prod[1], prod[0]))
        log('scraped {} products'.format(len(product_objects)))
        return product_objects

    def run(self):
        log('monitor thread started')
        # get initial products
        self.products = self.scrape_products()
        for prod in self.products:
            prod.get_variants(self.s)
            sleep(3.0)

        # for prod in self.products:
        #     for keyset in self.keywords['sets']:
        #         if

