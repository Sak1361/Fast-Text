import requests, re
from bs4 import BeautifulSoup

def crawling(f_path1,f_path2):
    url_positive = "http://meigen.keiziban-jp.com/ポジティブ"
    url_negative = "http://meigen.keiziban-jp.com/ネガティブ"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    response = requests.get(url_positive,headers=headers)
    response.encoding = response.apparent_encoding
    with open(f_path1,'w',encoding="utf-8") as f:
        f.write(response.text)
    response = requests.get(url_negative,headers=headers)
    response.encoding = response.apparent_encoding
    with open(f_path2,'w',encoding="utf-8") as f:
        f.write(response.text)

def scraping(filename):
    html = open(filename,'r')
    soup = BeautifulSoup(html, "html.parser")
    for res in soup.find_all(class_="wpcr_inactive"):
        print(res)
    #res = soup.find(class_="wpcr_inactive").text
    #print(res)

if __name__ == "__main__":
    #crawling("a.html","b.html")
    #scraping("a.html")
    scraping("b.html")