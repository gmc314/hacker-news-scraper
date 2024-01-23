import requests
from bs4 import BeautifulSoup
from pprint import pprint


def request_page_num(num):
    return requests.get(f'https://news.ycombinator.com/news?p={num+1}')


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda x: x["Points"], reverse=True)


def create_custom_hn(titles, subtext):
    hn = []
    for idx, item in enumerate(titles):
        title = item.getText()
        link = item.select('a')[0].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote) != 0:
            points = int(vote[0].getText().replace(' points', ''))
            if points >= 100: 
                hn.append({"Title":title, "Link":link, "Points":points})
    return sort_stories_by_votes(hn)


def get_hn_top_stories_by_page(number_of_pages): 
    stories_list = []

    for i in range(number_of_pages):
        res = request_page_num(i)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        titles = soup.select('.titleline')
        subtext = soup.select('.subtext')

        stories = create_custom_hn(titles, subtext)
        stories_list.append(stories)    
    
    return stories_list


def flatten_list_of_lists(lol):
    flat_list = []

    for lst in lol:
        flat_list.extend(lst)
    
    return flat_list


pprint(flatten_list_of_lists(get_hn_top_stories_by_page(4)))