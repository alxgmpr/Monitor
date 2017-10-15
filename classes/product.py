# coding = utf-8

import requests

from logger import Logger

L = Logger()
log = L.log


class Product:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.variants = {}
        self.price = '0.00'
        L.name = self.url

    def get_variants(self, session):
        # open product json
        r = session.get(
            '{}.json'.format(self.url)
        )
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            log('error {} on product json request'.format(r.status_code))
        prod_json = r.json()
        for var in prod_json['product']['variants']:
            self.variants['title'] = var['id']
