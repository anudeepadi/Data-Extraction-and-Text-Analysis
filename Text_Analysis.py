    from itertools import count
    from string import punctuation
    import pandas as pd
    import os
    from nltk.corpus import stopwords
    from nltk.tokenize import sent_tokenize, word_tokenize
    import re
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

    class TextAnalysis():
        def __init__(self):
            self.stop_words = [stopwords.words('english')]
            self.punctuation = list(punctuation)
            self.positive = []
            self.negative = []

        def get_stop_wrods(self):
            path2 = "C:/Users/anude/Downloads/intern_proj/StopWords"
            for root, dirs, files in os.walk(path2):
                for file in files:
                    with open(os.path.join(path2, file), "r") as f:
                        for line in f:
                            self.stop_words.extend(line.split('\n'))
            return self.stop_words

        def get_positive_negative_words(self):
            path1 =  "C:/Users/anude/Downloads/intern_proj/MasterDictionary"
            for root, dirs, files in os.walk(path1):
                for file in files:
                    if file == "positive-words.txt":
                        with open(os.path.join(path1, file), "r") as f:
                            for line in f:
                                self.positive.extend(line.split('\n'))
                    if file == "negative-words.txt":
                        with open(os.path.join(path1, file), "r") as f:
                            for line in f:
                                self.negative.extend(line.split('\n'))
            self.positive = list(set(self.positive))
            self.positive.remove('')
            self.negative = list(set(self.negative))
            self.negative.remove('')
            return self.positive, self.negative

        def remove_punctuation(self, text):
            return "".join([char for char in text if char not in self.punctuation])

        def remove_stop_words(self, text):
            return " ".join([word for word in text.split() if word not in self.stop_words])

        def remove_urls(self, text):
            return re.sub(r'http\S+', '', text)

        def preprocess_task(self, text):
            text = self.remove_punctuation(text)
            text = self.remove_stop_words(text)
            text = self.remove_urls(text)
            return text

        def postive_negative_calculate(self, text):
            text = self.preprocess_task(text)
            no_of_words = self.get_word_count(text)
            positive_words = []
            negative_words = []
            for word in self.positive:
                if word in text:
                    positive_words.append(word)
            for word in self.negative:
                if word in text:
                    negative_words.append(word)
            positive_words_count = len(positive_words)
            negative_words_count = len(negative_words)
            subjectivity = (positive_words_count + negative_words_count) / (no_of_words + 0.000001)
            polarity = (positive_words_count - negative_words_count) / ((positive_words_count + negative_words_count) + 0.000001)
            return positive_words_count, negative_words_count, subjectivity, polarity

        def get_readability_score(self, text):
            no_of_words = self.get_word_count(text)
            percentage_of_complex_words = self.get_complex_words(text)
            percentage_of_complex_words = percentage_of_complex_words / no_of_words if no_of_words > 0 else 0
            fog_index = 0.4 * (self.get_avg_words_per_sentence(text) + percentage_of_complex_words)
            return self.get_avg_sentence_length(text), percentage_of_complex_words, fog_index
        
        def get_syllables(self, text):
            vowels=['a','e','i','o','u']
            no_of_syllables = 0
            count = 0
            cleaned_text=str(text).split()
            for i in cleaned_text:
                x=[char for char in i]
                items = set(vowels)
                y= len([i for i in x if i in items])
                no_of_syllables = no_of_syllables + y
                count = count + 1
            return no_of_syllables / count if count > 0 else 0

        def get_complex_words(self, text):
            text = self.preprocess_task(text)
            cleaned_text=str(text).split()
            vowels=['a','e','i','o','u']
            complex_word_count = 0
            for i in cleaned_text:
                x=[char for char in i]
                items = set(vowels)
                y= len([i for i in x if i in items])
                if y>2:
                    complex_word_count = complex_word_count + 1
            return complex_word_count

        def get_avg_words_per_sentence(self, text):
            sen = self.get_sentence_count(text)
            return self.get_word_count(text) / sen if sen > 0 else 0

        def get_word_count(self, text):
            text = self.preprocess_task(text)
            return len(text)

        def countfunc(self, store, words):
            score = 0
            for x in words:
                if(x in store):
                    score = score+1
            return score

        def get_personal_pronouns(self, text):
            text = self.preprocess_task(text)
            regex = re.compile(r'I|we|my|ours|(?-i:us)', re.I)
            pronouns_count = regex.findall(str(text))
            no_of_pronous=len(pronouns_count)
            return no_of_pronous

        def get_sentence_count(self, text):
            return len(sent_tokenize(text))

        def get_avg_sentence_length(self, text):
            no_of_words = self.get_word_count(text)
            return no_of_words / self.get_sentence_count(text) if no_of_words > 0 else 0

        def get_avg_word_length(self, text):
            chars = 0
            total_words = " ".join([word for word in text])
            for word in text:
                for char in word:
                    chars += 1
            return int(chars) / len(total_words) if len(total_words) > 0 else 0

        def get_urls(self, id):
            df = pd.read_excel("C:/Users/anude/Downloads/intern_proj/Input.xlsx")
            ids = [id for id in df.URL_ID]
            articles = [article for article in df.URL]
            return articles[int(id) - 1]

        def do_analysis_output_to_excel(self):
            df = pd.DataFrame()
            path = "C:/Users/anude/Downloads/intern_proj/data"
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith(".txt"):
                        with open(os.path.join(path, file), "r", encoding="utf-8") as f:
                            text = f.read()
                            id = file.split(".")[0]
                            url = self.get_urls(id)
                            positive, negative, polarity, subjectivity = self.postive_negative_calculate(text)
                            complex_words = self.get_complex_words(text) 
                            syllables = self.get_syllables(text)
                            average_sentence_length, percentage_of_complex_words, fog_index = self.get_readability_score(text) if not None else 0, 0, 0
                            avg_words_per_sentence = self.get_avg_words_per_sentence(text)
                            avg_word_length = self.get_avg_word_length(text)
                            personal_pronouns = self.get_personal_pronouns(text)   
                            dic = {"URL ID": id,"URL": url,"POSITIVE SCORE":positive,"NEGATIVE SCORE":negative,"POLARITY SCORE":polarity,"SUBJECTIVITY SCORE":subjectivity, "AVG SENTENCE LENGTH":average_sentence_length, "PERCENTAGE OF COMPLEX WORDS":percentage_of_complex_words, "FOG INDEX":fog_index, "AVG NUMBER OF WORDS PER SENTENCE":avg_words_per_sentence, "COMPLEX WORD COUNT":complex_words, "WORD COUNT":self.get_word_count(text),"SYLLABLE COUNT PER WORD":syllables, "PERSONAL PRONOUNS":personal_pronouns, "AVG WORD LENGTH":avg_word_length}
                            df = df.append(dic, ignore_index=True)
                            print(dic["FOG INDEX"])
            df.to_excel("C:/Users/anude/Downloads/intern_proj/Output.xlsx", index=False)
            print("Done")
            return df

                    
    if __name__ == "__main__":
        scrapper = Scrapper('Input.xlsx')
        scrapper.extract_data()
        analysis = TextAnalysis()
        analysis.get_stop_wrods()
        analysis.get_positive_negative_words()
        analysis.do_analysis_output_to_excel()