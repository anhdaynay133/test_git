import luigi
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
from sqlalchemy import select

from Create_DB import session,Article, Category,


def get_html_document(url) :
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    return soup

class Get_data_input(luigi.Task):

    def output(self):
        return luigi.LocalTarget("data.json")

    def run(self):
        f = open("input.txt", "r")
        url = f.read()
        soup_post = get_html_document(url)

        # Get title information
        title_tag = soup_post.find("h1", attrs={"class": "article-title"})
        # Get description information
        description_tag = soup_post.find("h2",attrs = {"class":"sapo"})
        # Get category information
        div_cates = soup_post.find("div",  attrs = {"class":"bread-crumbs fl"})
        tag_ul = div_cates.find("ul")
        tag_li = tag_ul.find_all("li")
        for i in tag_li:
            category_tag = i.find('a').get_text()
            break
        date_time = soup_post.find("div", attrs={"class": "date-time"}).get_text().strip("GMT+7").rstrip()
        date_public = datetime.strptime(date_time, '%d/%m/%Y %H:%M').strftime("%Y-%m-%d %H:%M")
        collect_data = {
            "title": title_tag.get_text(),
            "description": description_tag.get_text(),
            "category": category_tag,
            "url": url,
            "date_public" : date_public

        }
        with self.output().open("w") as f:
            json.dump(collect_data, f, indent=4, ensure_ascii=False)


class Clean_data(luigi.Task):

    def requires(self):
        return Get_data_input()

    def output(self):
        return None

    def run(self):
        return None


class Recommend(luigi.Task):

    def requires(self):
        return Clean_data()

    def output(self):
        return luigi.LocalTarget("output.text")

    def run(self):
        f = open(r'D:/Python_Code/A1_TRAINING_NongVanToan/Phase1/data.json', encoding="utf-8-sig")
        data = json.load(f)
        session.add(data)
        session.commit()


# stmt = select(Article.title, Article.url, Category.category_name).join(Category)
#
# for row in session.execute(stmt):
#     with open('data_raw.json', 'a', encoding='utf-8-sig') as f:
#         f.write(str(row) + '\n')
#
#     if data_raw['Category'] == stmt.category:
#         pass
#




#DEMO1.PY
import json
from Create_DB import Article_input, session

data_import = []
f = open(r'D:/Python_Code/A1_TRAINING_NongVanToan/Phase1/data.json', encoding="utf-8-sig")

data_import.append(json.load(f))


# Add objects article
article_input =  session.query(Article_input).filter(Article_input.title == data_import['title']).first()
if not article_input:
    article_input = Article_input(title = data_import['title'] ,description = data_import['description'], category = data_import['category'],url = data_import['url'] , date_public = data_import['date_public'])
    session.add(article_input)
    session.commit()

