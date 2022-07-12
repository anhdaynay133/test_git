import requests

from bs4 import BeautifulSoup
response = requests.get("https://tuoitre.vn/xe.htm")

objects  = BeautifulSoup(response.text, "html.parser")
#Find tag ul
tag_ul = objects.find("ul", attrs={"class":"list-news-content"})
#Find tag li
tag_li = tag_ul.find_all("li", attrs={"class": "news-item"})
 
result = []


chars = []
codes = []
f = open("Chars.txt", 'r', errors="ignore")
Tables_chars = f.read().split("\n")
file = open("Codes.txt", 'r', errors="ignore")
Tables_codes = file.read().split("\n")

for i in Tables_chars:  
    chars.append(i) 
for j in Tables_codes:  
    codes.append(j)


# Use loop for in tag li to find title  
for i in tag_li:  
    title = i.find('h3').a
    description = i.find("p") 
    img_data = i.find("img")

    respon = requests.get(img_data['src'])
    with open ("Imgs/" + img_data['src'].split("/")[-1], 'wb') as f:
        f.write(respon.content)  
        f.close()

    collection_data = {"Title " : title.get_text() , 
    "Description ":description.get_text() ,                     #encode('cp850','replace').decode('cp850')
    "Image ":img_data['src'] }
    result.append(collection_data)

files = open("data.txt", 'w', encoding='utf-8')
for elements in result : 
    files.write(str(result))
files.close()


#  Replace special character in name and scores 
