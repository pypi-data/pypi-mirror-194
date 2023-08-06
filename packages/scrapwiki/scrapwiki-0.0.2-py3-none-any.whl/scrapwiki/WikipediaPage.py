import requests
from bs4 import BeautifulSoup

class read_url:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.title = None
        self.paragraph = None

    def fetch(self):
	    html = requests.get(self.url).text

	    soup = BeautifulSoup(html, "html.parser")
	    self.soup = str(soup)

	    title = soup.find("h1", {"class": "firstHeading"}).text
	    self.title = title

	    paragraph_elem = soup.findAll("p")
	    if paragraph_elem:
	    	paragraph = []
	    	for elem in paragraph_elem:
	    		text = elem.text
	    		paragraph.append(text.replace('\n',''))
	    	if len(paragraph)<=3:
	    		paragraph = None
	    else:
	    	paragraph = None

	    self.paragraph = paragraph

    def __str__(self):
    	if self.paragraph == None:
    		return "Wikipedia does not have an article with this exact name : " + self.title
    	else:
    		return "WikipediaPage :\t " + self.title + "\nURL :\t " + self.url

def test():
	Page_url = "https://en.wikipedia.org/wiki/Cat"
	Page = read_url(Page_url)
	Page.fetch()
	print(Page)

if __name__ == "__main__":
    test()