#Задача:
# необходимо обойти все публикации в блоге и сохранить в MongoDB следующую информацию:
# Заголовок статьи, ссылка на статью, дата публикации (только дата без времени), Имя автора
import pymongo
from bs4 import BeautifulSoup
import requests
from time import sleep
import random

#Обходим все наши посты
def get_posts_from_page(url_curent):

    page = requests.get(url_curent)
    soup = BeautifulSoup(page.text, "html.parser")
    posts = []
    for post in soup.find_all('div','post-item'):
        tag = post.find('a','post-item__title')
        #ссылка
        post_url = tag.attrs['href']

        #имя статьи
        post_name = tag.string

        #Дата публикации
        post_date = post.find('div','small m-t-xs').string

        #Для получения имени автора нам надо провалится внутрь статьи
        #post_author = ''
        page_post = requests.get(base_url+post_url)
        soup_post = BeautifulSoup(page_post.text, "html.parser")
        post_author = soup_post.find('article','blogpost__article-wrapper').find(itemprop='author').string

        posts.append({'title':post_name,'url':base_url+post_url,'author':post_author,'date':post_date})

    #Проверим, есть ли там у нас что ещё дальше смотреть
    link_pagination = soup.find('ul', 'gb__pagination').find_all('a')
    link_pagination = link_pagination[len(link_pagination) - 1].attrs

    if 'href' in link_pagination:
        next_url = link_pagination['href']
    else:
        next_url = ''

    return {'next':next_url,'data':posts}

#=========================================================================================
#Соеденине с базой будет вот таким простым
client = pymongo.MongoClient("mongodb://dbUser:Froskur1234@cluster0-shard-00-00-llgb1.gcp.mongodb.net:27017,cluster0-shard-00-01-llgb1.gcp.mongodb.net:27017,cluster0-shard-00-02-llgb1.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client['test']
coll = db.geekbrains2

base_url = 'https://geekbrains.ru'
next_url = '/posts'

while next_url != '':
    print(f'Обрабатываю {base_url}{next_url} ...')
    res = get_posts_from_page(base_url + next_url)
    coll.insert_many(res['data'])
    next_url = res['next']
    time_sleep = random.randint(1,8)
    print(f'Замираю на {time_sleep} секунд...')
    sleep(time_sleep)

print(f'Завершено!')






#print(res)

