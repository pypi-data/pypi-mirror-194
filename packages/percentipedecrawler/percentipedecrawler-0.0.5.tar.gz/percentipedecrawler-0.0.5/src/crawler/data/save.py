from sqlalchemy import text
from sqlalchemy.orm import Session
from .database import get_engine
from .models import Crawls
from crawler.parser import strip_tags
import markdownify


def save(crawl_id, domain, url, html):
    engine = get_engine()
    with Session(engine) as session:
        text = strip_tags(html)
        md = markdownify.markdownify(text, heading_style="ATX")
        crawl = Crawls(crawl_id=crawl_id, domain=domain, url=url,
                       html=html, markdown=md, text=text)
        session.add(crawl)
        return session.commit()
