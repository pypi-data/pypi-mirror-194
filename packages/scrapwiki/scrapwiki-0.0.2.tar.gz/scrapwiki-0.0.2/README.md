# scrapwiki
A python package for scrap Wikipedia page. Fetch title, paragraph or entire page html
```
pip install scrapwiki
```
# Wikipedia page example
![alt text](https://github.com/Krittipoom/scrapwiki/blob/main/scrapwiki/wikipedia%20page%20of%20cat.png)
https://en.wikipedia.org/wiki/Cat

# Code example
```
from scrapwiki import read_url

page = read_url("https://en.wikipedia.org/wiki/Cat")
page.fetch()
```
```
print(page)
```

```ruby
#WikipediaPage :	 Cat
#URL :	 https://en.wikipedia.org/wiki/Cat
```
```
print(page.paragraph)
```
```ruby
#Return all paragraph <p></p>
```
```
print(page.soup)
```
```ruby
#Return entire html
```
