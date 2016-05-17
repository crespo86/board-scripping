# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET
import codecs
import csv


#WAY_TAGS_FIELDS = ['aid', 'title', 'uid', 'nick', 'date', 'viewV']
WAY_TAGS_FIELDS = ['aid', 'title', 'uid', 'nick', 'date', 'viewV', 'word','reply']



makefile = []

def url(n):
#    URL = 'http://mlbpark.donga.com/mlbpark/b.php?p='+str(n)+'&amp;m=list&amp;b=bullpen2&amp;query=&amp;select=title&amp;user='
    URL = 'http://mlbpark.donga.com/mlbpark/b.php?p='+str(n)+'&m=list&b=kbotown2&query=&select=title&user='
    soup = BeautifulSoup(urlopen(URL), "lxml")
    return soup

def get_attr(line):

    database = {'aid' : 0,
                'title' : '',
                'uid' : '',
                'nick': '',
                'date': '',
                'viewV': 0,
                'word': 'NULL', #for kbotown
                'reply': 0  #for kbotown
                }
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
#                            database['title'] = b['alt']
                            if str(b.text)[-5:-1].find('[') == -1:
                                database['title'] = str(b.text)[0:-1]
                            else:
                                database['title'] = str(b.text)[0:-4]
                                database['reply'] = str(b.text)[str(b.text).rfind('[')+1:-1]
                            for last in b:
                                if last.name == 'span' and last['class'] == ['word']:
                                    database['word'] = last.string

                except:
                    pass
    return database


def test():

    with codecs.open('mlbstat.csv', 'w') as f:  # Just use 'w' mode in 3.x
        mlb_writer = csv.DictWriter(f, WAY_TAGS_FIELDS)
        mlb_writer.writeheader()

        for num in range(1,1700):
            n = 1
            for line in url(1+30*(num-1)).find_all('tr'):
#                if n <= 4:
                if n <= 3:
                    n += 1
                else:
                    try:
#                        if n < 35:
                        if n < 34:
                            mlb_writer.writerow(get_attr(line))
                            n += 1
                    except:
                        pass


if __name__ == '__main__':
    test()
