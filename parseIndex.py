#!/bin/python

import bs4

def parseHtml(HTML):
    soup = bs4.BeautifulSoup(HTML, 'html.parser')
    links = soup.find_all('a')[1:]

    urls = [ l.getText() for l in links]
    return urls
