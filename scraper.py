import requests
from bs4 import BeautifulSoup
from pprint import pprint

res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')

titles = soup.select('.titleline')
subtext = soup.select('.subtext')

def rank_hn_articles(titles, subtext):
    hn = []
    for idx, item in enumerate(titles):
        title = item.getText()
        link = item.select('a')[0].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote) != 0:
            points = int(vote[0].getText().replace(' points', ''))
            if points >= 100: 
                hn.append({"Title":title, "Link":link, "Points":points})
    return hn
