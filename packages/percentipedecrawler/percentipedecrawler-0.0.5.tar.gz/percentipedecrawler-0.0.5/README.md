# Crawler

Crawler is a simple, blocking Python Crawler that is the backbone of a few other projects.

You're welcome to use it, but it's only as modular as we've needed it to be, which is to say, probably not fit for projects that aren't built with this in mind.

It works pretty simply.

## Installation

```
pip install crawler@git+https://github.com/bmelton/python-crawler@stable
```

Crawler depends on MySQL, so you'll need to have the requisite mysql client libraries in order for pymysql to work.
On OSX, this is solved for with brew

```
brew install mysql
```

## Usage

```
from crawler import crawler
crawler = Crawler(domain="https://yourdomain.com", sitemap="https://yourdomain.com/sitemap.xml")
crawler.run()
```

If you just want to fetch a given page, create an instance of the crawler and call it like this:

```
crawler.fetch_page(url="https://yourdomain.com/blog/title")
```

The `init` will create a nanoid `crawl_id` so that when results are persisted, they'll be associated to a given crawl, to make it easy for reports to be built against crawls and such.

## Persistence

It requires a MySQL config to work, which you can trivially solve for with this docker command:

```
docker run -d -p 33060:3306 -e MYSQL_ROOT_PASSWORD=<PASSWORD> -v mysql:/var/lib/mysql  --name mysql mysql
```
