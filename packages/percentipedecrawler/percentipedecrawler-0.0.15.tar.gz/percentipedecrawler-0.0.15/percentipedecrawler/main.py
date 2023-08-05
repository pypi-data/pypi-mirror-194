import logging
from Crawler import Crawler

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
    level=logging.INFO
)


if __name__ == "__main__":
    domain = "https://sureisfun.com"
    sitemap = "https://sureisfun.com/sitemap.xml"

    crawler = Crawler(domain=domain, sitemap=sitemap)
    crawler.run()
