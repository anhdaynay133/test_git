import luigi
from bs4 import BeautifulSoup
import requests
# from create_db  import Article, Category, Keyword, session, engine
import json


def get_html_document(url) :
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    return soup

class Get_data_input(luigi.Task):

    def output(self):
        return luigi.LocalTarget("output.json")

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

        collect_data = {
            "title": title_tag.get_text(),
            "description": description_tag.get_text(),
            "category": category_tag,
            "url": url,
            "date_time" : date_time

        }
        with self.output().open("w") as f:
            json.dump(collect_data, f, indent=4, ensure_ascii=False)


class Clean_data(luigi.Task):

    file_final = "/mnt/d/DACC/A1_TRAINING_NongVanToan/Phase1/output.json"
    def requires(self):
        return Get_data_input()

    def output(self):
        return luigi.LocalTarget("output.json")

    def run(self):
        with self.output().open( "r") as file:
            data = json.load(file)
            # Convert to standard form in the database
            data['date_time'] = data['date_time'].strptime(data['date_time'], '%d/%m/%Y %H:%M').strftime("%Y-%m-%d %H:%M")
