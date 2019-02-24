from bs4 import BeautifulSoup
import requests
from pprint import *


def get_news(url, n_pages=1):
    all_news = []

    response = requests.get(url)
    if not response.ok:
        assert 'WRONG URL'

    while n_pages > 0:
        html_text = response.text
        all_page_info = extract_next_page(html_text)

        if n_pages < len(all_page_info):
            print(all_page_info[:n_pages])
            all_news.extend(all_page_info[:n_pages])
        else:
            all_news.extend(all_page_info)

        n_pages -= len(all_page_info)

    return all_news
#

def extract_news(html_text):
    page = BeautifulSoup(html_text, 'html.parser')
    table = page.table.findAll('table')[1]

    all_titles_row = table.findAll('tr', {'class': 'athing'})
    all_titles = [title.findAll('td')[2].a.text for title in all_titles_row]
    all_titles_url = [title.find('a', {'class': 'storylink'})['href'] for title in all_titles_row]

    all_info_row = table.findAll('td', {'class': 'subtext'})
    all_page_info = []

    for index, post in enumerate(all_info_row):
        points = int(post.find('span', {'class': 'score'}).text.split()[0])
        author = post.find('a', {'class': 'hnuser'}).text
        comments = post.findAll('a')[-1].text

        all_page_info.append({
            'author': author,
            'points': points,
            'comments': 0 if comments == 'discuss' else int(comments.split()[0]),
            'title': all_titles[index],
            'url': all_titles_url[index]
        })

    return all_page_info


def extract_next_page(html_text):
    page = BeautifulSoup(html_text, 'html.parser')
    more_link = page.find('a', {'class': 'morelink'})
    return more_link['href']


if __name__ == '__main__':
    url = "https://news.ycombinator.com/newest"
    pprint(get_news(url))
