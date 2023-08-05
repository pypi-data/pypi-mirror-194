from sqlalchemy.orm import Session
from database import get_engine
from models import Crawls
import markdownify
from bs4 import BeautifulSoup


def strip_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    head = soup.find("head")
    head.clear()
    return soup.body.get_text()


def save(crawl_id, domain, url, html):
    engine = get_engine()
    with Session(engine) as session:
        text = strip_tags(html)
        md = markdownify.markdownify(text, heading_style="ATX")
        crawl = Crawls(crawl_id=crawl_id, domain=domain, url=url,
                       html=html, markdown=md, text=text)
        session.add(crawl)
        return session.commit()
