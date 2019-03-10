from bs4 import BeautifulSoup
import requests
import time


def get_news(url, n_pages=1):
    all_news = []

    while n_pages > 0:
        print(url)
        response = requests.get(url)
        if not response.ok:
            assert 'WRONG URL'

        html_text = response.text

        if html_text == '':
            time.sleep(60)
            continue

        all_page_info = extract_news(html_text)

        all_news.extend(all_page_info)

        url = extract_next_page(html_text)
        n_pages -= 1
        time.sleep(30)

    return all_news


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
    return 'https://news.ycombinator.com/' + more_link['href']


if __name__ == '__main__':
    url = "https://news.ycombinator.com/newest"
