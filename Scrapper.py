import requests
from bs4 import BeautifulSoup
import pandas as pd

class Scrapper():
    def __init__(self, input_file):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',}
        self.input_file = input_file

    def extract_data(self):
        data = pd.read_excel(self.input_file)
        url_list = [url for url in data.URL]
        id_list = [id for id in data.URL_ID]
        
        for url in url_list:
            r = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            if self.get_text(soup) is not None:
                text = self.get_text(soup).text
                self.save_to_file(str(id_list[url_list.index(url)]), text)
            else:
                text = 'No text'
        return None

    def get_title(self, soup):
        return soup.find('h1', {'class' : 'entry-title'})

    def get_text(self, soup):
        return soup.find('div', {'class' : "td-post-content"})

    def get_all(self):
        return self.soup.find_all()
    
    def save_to_file(self, file_name, text):
        f_path = 'C:/Users/anude/Downloads/intern_proj' + '/new_data/' + file_name + '.txt'
        file = open(f_path, 'w', encoding="utf8")
        file.write(text)
        file.close()
        return None


if __name__ == "__main__":
    scrapper = Scrapper('Input.xlsx')
    scrapper.extract_data()