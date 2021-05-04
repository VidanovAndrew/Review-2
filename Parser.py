import requests
import lxml
from bs4 import BeautifulSoup
from pydantic import BaseModel, ValidationError
import html
from datetime import datetime
from collections import Counter


def parseArticle(paragraphs):
    topNews = []
    for paragraph in paragraphs:
        text = ' '
        try:
            article = BeautifulSoup(requests.get(paragraph.attrs["href"]).text, 'lxml')
            trash = article.select('a')
            for item in trash:
                item.decompose()
            for it in article.find_all('p'):
                # print(it.text.strip('\n')) # text.strip('\n')
                if (it.text.strip('\n').strip(' ')[0:18] != "Подписка отключает" and
                        it.text.strip('\n').strip(' ')[0:18] != "Всего 99₽ в месяц " and
                        it.text.strip('\n').strip(' ')[0:18] != "Продлевается автом"):
                    text = text + (html.unescape(it.text)).strip('\n').strip(' ') + '\n'
                    # print(it.text.strip('\n').strip(' '))

        except BaseException:
            pass
        if paragraph.text.strip('\n') != '':
            try:
                content = html.unescape(text)
                index = 0
                while (len(Counter(content.split()).most_common()) > index)\
                        and len(Counter(content.split()).most_common()[index][0]) <= 3:
                    index += 1
                topNews.append([str(datetime.now())[:10], html.unescape(paragraph.text).strip('\n').strip(' '),
                                content, paragraph.attrs["href"],
                                Counter(content.split()).most_common()[index][0],
                                Counter(content.split()).most_common()[index][1]
                                ])
            except BaseException as e:
                print(paragraph, "ERRRRoooR: ", e)
    print(topNews)
    return topNews


class Category(BaseModel):
    name_: str
    reference_: str
    links_catcher_: dict
    subcategories_: dict

    def my_parse(self):
        parsed_list = []
        for subcat in self.subcategories_:
            response = requests.get(self.reference_ + self.subcategories_[subcat])
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            paragraphs = soup.find_all('a', attrs=self.links_catcher_)
            parsed_list.append(parseArticle(paragraphs))
            break
        return parsed_list[0]


def ParseMainRBC():
    response = requests.get('https://www.rbc.ru')
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    paragraphs = []
    for i in range(1, 15):
        paragraphs.append(soup.find('a', attrs={"data-rm-position": i}))
    return parseArticle(paragraphs)


def god_parse():
    with open('Parse_list.txt', 'r') as f:
        lines = f.readlines()
        all_parsed = []
        for line in lines:
            try:
                category = Category.parse_raw(line)
                all_parsed.append(category.my_parse())
            except ValidationError as e:
                print(e.json())
        return all_parsed


def parse_topic(name_topic):
    flag = 0
    index = 0
    with open('topic_names.txt', 'r') as f:
        lines = f.readlines()
        for i in lines:
            if i.strip() == name_topic:
                flag = 1
                break
            index += 1
    result = None
    if flag:
        with open('Parse_list.txt', 'r') as f:
            lines = f.readlines()
            all_parsed = []
            try:
                category = Category.parse_raw(lines[index])
                result = category.my_parse()
            except ValidationError as e:
                print(e.json())
    return result

'''
start = datetime.now()
god_parse()
print(datetime.now() - start)
'''