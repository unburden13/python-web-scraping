import requests
from bs4 import BeautifulSoup  # or Scrapy for more features and massive processing
import pprint



def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k:k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links): # enumerate allows give an index to each iteration
        title = links[idx].getText()
        href = links[idx].contents[0].get('href', None)  # grab by attribute on each element
        vote = subtext[idx].select('.score')  # because a link can have no points
        if len(vote):
            points = int(vote[0].getText().replace(' points',''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return hn


def scrape_hn(pages):
    hn = []
    for page in range(1,int(pages)+1):
        response = requests.get(f'https://news.ycombinator.com/news?p={page}')
        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.select('.titleline')  # grab by css selector
        subtext = soup.select('.subtext')  # makes print a little bit prettier

        hn.extend(create_custom_hn(links, subtext))
    return hn


pages = input('How many pages do you want to scrape? ')
result = scrape_hn(pages)


pprint.pprint(sort_stories_by_votes(result))