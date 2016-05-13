# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET
import codecs
import csv


WAY_TAGS_FIELDS = ['aid', 'title', 'uid', 'nick', 'date', 'viewV']
database = {'aid' : 0,
            'title' : '',
            'uid' : '',
            'nick': '',
            'date': '',
            'viewV': 0
            }

makefile = []

def url(n):
#    URL = 'http://mlbpark.donga.com/mlbpark/b.php?p='+str(n)+'&amp;m=list&amp;b=bullpen2&amp;query=&amp;select=title&amp;user='
    URL = 'http://mlbpark.donga.com/mlbpark/b.php?p='+str(n)+'&m=list&b=kbotown2&query=&select=title&user='
    soup = BeautifulSoup(urlopen(URL), "lxml")
    return soup

def get_attr(line):
    m = 1
    for a in line:
        if m == 1:
            database['aid'] = a.string
            m += 1

        else:
            for b in a:
                try:
                    if b.name == 'span':
                        if b['class'] == ["photo"]:
                            database['uid'] = (b.find('a')['data-uid'])
                        elif b['class'] == ["date"]:
                            database['date'] = b.string
                        elif b['class'] == ['viewV']:
                            database['viewV'] = b.string
                        elif b['class'] == ['nick']:
                            database['nick'] = b.string
                    else:
                        if b.name == 'a':
                            database['title'] = b['alt']
                except:
                    pass
    return database


def test():

    with codecs.open('kbotown.csv', 'w') as f:  # Just use 'w' mode in 3.x
        mlb_writer = csv.DictWriter(f, WAY_TAGS_FIELDS)
        mlb_writer.writeheader()

        for num in range(1,10):
            n = 1
            for line in url(1+30*(num-1)).find_all('tr'):
                if n <= 4:
                    n += 1
                else:
                    try:
                        if n < 35:
                            mlb_writer.writerow(get_attr(line))
                            n += 1
                    except:
                        pass


if __name__ == '__main__':
    test()
