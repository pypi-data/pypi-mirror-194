from bs4 import BeautifulSoup


def strip_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    head = soup.find("head")
    head.clear()
    return soup.body.get_text()
