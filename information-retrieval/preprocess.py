from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer, SnowballStemmer
from nltk.tag import pos_tag

import nltk
import string
import simplemma

from config import config


nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

class Preprocess:

    def __init__(self) -> None:
        self.text = ''
        self.stop_words = {
            'en': stopwords.words('english'),
            'cs': []
        }
        with open ("czech_stopwords.txt", "r") as f:
            self.stop_words['cs'] = f.read().splitlines()

    def preprocess(self, text, lang, run) -> list:
        run_config = config[lang][run]
        self.text = text
        if run_config['lowercase']:
            self.text = self.text.lower()
        if run == 'run-0':
            words = self.text.split()
        else:
            words = word_tokenize(self.text) 
        table = str.maketrans('', '', string.punctuation)
        tokenized_text = [w.translate(table) for w in words]
        tokenized_text = [token for token in tokenized_text if len(token) > 0]
        if run_config['lemmatize']:
            tokenized_text = self.perform_lemmatization(tokenized_text, lang)
        if run_config['stemming'] and lang == 'cs':
            tokenized_text = self.perform_stemming(tokenized_text, lang)
        if run_config['remove_stopwords'] and lang == 'cs':
            tokenized_text = self.remove_stopwords(tokenized_text, lang)
        return tokenized_text

    def remove_stopwords(self, tokenized_text, lang) -> list:
        tokens_without_stopwords = [
            word for word in tokenized_text if word not in self.stop_words[lang]]
        return tokens_without_stopwords

    def perform_stemming(self, tokenized_text, lang) -> list:
        if lang == 'en':
            stemmer = SnowballStemmer('english')
            tokens = [stemmer.stem(token) for token in tokenized_text]
        return tokens

    def perform_lemmatization(self, tokens, lang) -> list:
        lemmatized_text = [simplemma.lemmatize(token, lang) for token in tokens]
        return lemmatized_text

