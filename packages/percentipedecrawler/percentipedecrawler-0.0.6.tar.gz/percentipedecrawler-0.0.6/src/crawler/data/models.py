from sqlalchemy import Column, DateTime, Integer, String, TIMESTAMP, TEXT, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()
metadata = Base.metadata


class Crawls(Base):
    __tablename__ = "web_crawls"

    id = Column(Integer, primary_key=True)
    crawl_id = Column(String(10, "utf8_unicode_ci"),
                      nullable=False, index=True)
    domain = Column(String(255, "utf8_unicode_ci"), nullable=False, index=True)
    url = Column(String(255, "utf8_unicode_ci"), nullable=True, index=True)
    html = Column(TEXT, nullable=True, index=False)
    markdown = Column(TEXT, nullable=True, index=False)
    text = Column(TEXT, nullable=True, index=False)
    crawl_time = Column(DateTime(timezone=True), server_default=func.now())
