# coding = utf-8

# Shopify Monitor
# By Alex Gompper https://github.com/alxgmpr

from classes.logger import Logger
from classes.monitor import Monitor

def main():
    log = Logger('main').log

    log('starting monitor')

    with open('sites.txt') as sitelist:
        sites = sitelist.read().splitlines()
    log('loaded {} sites to monitor'.format(len(sites)))

    with open('proxies.txt') as proxylist:
        proxies = proxylist.read().splitlines()
    log('loaded {} proxies to monitor with'.format(len(proxies)))

    i = 0
    monitors = []
    for site in sites:
        monitors.append(Monitor(site))
        monitors[i].start()
        i += 1

if __name__ == '__main__':
    main()