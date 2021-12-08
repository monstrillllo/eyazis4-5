from bs4 import BeautifulSoup
import requests
from random import choice

url_ru = 'https://rustih.ru'
url_en = 'https://crazylink.ru/english/english-poetry.html'
url_authors = 'https://www.culture.ru/literature/persons'
url_authors_en = 'https://www.thefamouspeople.com/writers.php'
headers = {'user-agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
           'accept':
               'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9'}


def get_src(url):
    session = requests.session()
    response = session.get(url=url, headers=headers)
    return response.text


def get_random_poem_ru(src):
    soup = BeautifulSoup(src, 'lxml')
    pars = choice(soup.find_all('div', {'class': 'post-card-one'}))
    # print(pars)
    link = pars.find('a').get('href')
    return link


def get_text(src):
    soup = BeautifulSoup(src, 'lxml')
    pars = soup.find('div', {'class': 'entry-content poem-text'})
    result = ''
    for poem in pars:
        if poem.text.startswith('Анализ'):
            break
        # print(poem.text)
        result += poem.text
    print(result)
    return result


def get_random_poem_en(src):
    soup = BeautifulSoup(src, 'lxml')
    all_poems_div = soup.find('div', {'class': "list-posts clearfix"})
    all_poems = soup.find('ul', {'class': "list-unstyled lessons_list"}).find_all('div', {'class': 'item-content'})
    links = []
    for poem in all_poems:
        links.append(poem.find('a', {'class': 'read-more'}).get('href'))
    rand_poem = choice(links)
    poem_src = get_src(rand_poem)
    soup = BeautifulSoup(poem_src, 'lxml')
    poem_text_p = soup.find('div', {'id': 'main_text_in'}).find_all('p')
    poem_text = ''
    for p in poem_text_p:
        poem_text += p.text
        poem_text += '\n'
    return poem_text


def get_random_author_ru():
    main_page = get_src(url_authors)
    soup_main = BeautifulSoup(main_page, 'lxml')
    author_a = choice(soup_main.find_all('a', {'class': 'card-cover'}))
    link = 'https://www.culture.ru' + author_a.get('href')
    person_page = get_src(link)
    soup_person = BeautifulSoup(person_page, 'lxml')
    person_data = soup_person.find_all('div', {'class': 'attributes_block'})
    result = soup_person.find('h1', {'class': 'about-entity_title entity-title'}).text + '\n'
    for p in person_data:
        result += p.text + '\n'
    return result


def get_random_author_en():
    main_page = get_src(url_authors_en)
    soup = BeautifulSoup(main_page, 'lxml')
    author_info = choice(soup.find_all('article', {'class': "feature col-lg-12 col-md-12 col-sm-12 col-xs-12 eventstart internal_space"}))
    info_list = author_info.find_all('div', {'class': 'desc-q'})
    # print(author_info)
    result = author_info.find('a', {'class': 'tileLink'}).text + '\n'
    for p in info_list:
        result += p.text + '\n'
    return result
