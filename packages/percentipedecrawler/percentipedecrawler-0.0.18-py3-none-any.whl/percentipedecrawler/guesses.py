import logging
from urllib.parse import urljoin
from time import time

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
    level=logging.INFO
)


def guess_robots_url(url):
    logging.info("Guessing robots.txt url")
    return urljoin(url, "/robots.txt")


def guess_sitemap_url(url):
    logging.info("Guessing sitemap url")
    return urljoin(url, "/sitemap.xml")
