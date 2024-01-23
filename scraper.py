import requests
from bs4 import BeautifulSoup
from pprint import pprint


def request_page_num(num):
    """
    A function that returns the requests from the hackernews website 
    at a specific page number
    """
    
    return requests.get(f'https://news.ycombinator.com/news?p={num+1}')


def sort_stories_by_votes(hnlist):
    """A function that sorts the list of hacker news articles based 
    on how many points it has, in descending order"""
    return sorted(hnlist, key=lambda x: x["Points"], reverse=True)


def create_custom_hn(titles, subtext):
    """
    A function that converts the relevant HTML components of 
    the hacker news website of story title, the link, and the number of points, 
    to a list of dictionaries. Each dictionary contains the title, link, and points of 
    one story, and the stories are stored in the list. 
    Note: only stories with at least 100 points are stored.
    """
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


def get_hn_top_stories_by_page(number_of_pages): 
    """
    A function that returns the stories having at least 100 
    points of the first `number_of_pages` pages of the 
    hacker news website
    """
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
    """A simple function that merges all sublists within a list of lists into a single list"""
    flat_list = []

    for lst in lol:
        flat_list.extend(lst)
    
    return flat_list


pprint(sort_stories_by_votes(flatten_list_of_lists(get_hn_top_stories_by_page(4))))