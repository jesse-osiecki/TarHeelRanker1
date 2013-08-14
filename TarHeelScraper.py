#This code is written by Jesse J. Osiecki for Gary Bishop and associated @ UNC Chapel Hill

import urllib2
from BeautifulSoup import BeautifulSoup


class PageScraper:

    def __init__(self, url):
        self.title = ''
        self.body = []
        soup = BeautifulSoup(urllib2.urlopen(url).read())
        self.title = soup.title.string
        for anchor in soup.findAll('p'):
            self.body.append(anchor.text)

    def printPage(self):
        i = 0
        for b in self.body:
            print str(self.body[i])
            i += 1


class BookScraper:
    def __init__(self, url):
        self.pageScrapers = []
        pageIterator = 1
        while True:
            pString = str(url) + str(pageIterator) + '/'
            pageScraper = PageScraper(pString)
            pageIterator += 1
            if len(pageScraper.body) == 0:
                #you are on the last page and are done
                break
            else:
                self.pageScrapers.append(pageScraper)

    def printBook(self):
        for page in self.pageScrapers:
            page.printPage()


def testLib():
    t = BookScraper("http://tarheelreader.org/2013/07/10/how-ever-you-dance/")
    print t.pageScrapers[0].title
    t.printBook()
