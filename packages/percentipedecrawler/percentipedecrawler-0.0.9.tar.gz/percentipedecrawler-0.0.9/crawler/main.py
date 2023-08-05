import logging
from urllib.parse import urljoin
import requests
from lxml import etree
import urllib.robotparser
from crawl import guesses
from crawl.parser import strip_tags
from time import time
import markdownify
from data.save import save
from data.setup import setup
from nanoid import generate
from Crawler import Crawler

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
    level=logging.INFO
)


if __name__ == "__main__":
    domain = "https://fancasting.com"
    sitemap = "https://fancasting.com/sitemap.xml"

    crawler = Crawler(domain=domain, sitemap=sitemap)
    crawler.run()
