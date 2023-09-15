from preprocess import Preprocess
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool
from multiprocessing import Manager
import lxml
import re
import pandas as pd
from tqdm import tqdm

import warnings
warnings.filterwarnings(action='once')


class ParsedDocument:

    def __init__(self) -> None:
        self.preprocess = Preprocess()
        self.tags = {
            'en': ['DD', 'HD', 'DH', 'AU', 'BD', 'LD', 'TE', 'DC'],
            'cs': ['TITLE', 'HEADING', 'GEOGRAPHY', 'TEXT']
        },
        self.selected_tags = []
        self.doc_list = ''
        self.parsed_doc_list = Manager().list()
        self.topics = ''
        self.lang = ''
        self.doc_path = 'documents_'
        self.queries = []
        self.topic_title_map = {}
        self.run = ''
        self.parsed_docs = pd.DataFrame()

        tqdm.pandas()

    def process_documents(self, topics_path, doc_list_path, run):
        self.read_input(topics_path, doc_list_path, run)
        self.parse_docs_parallel()


    def read_input(self, topics_path, doc_list_path, run) -> None:
        with open(doc_list_path, "r") as f:
            self.doc_list = f.read().splitlines()
        if '_en' in doc_list_path:
            self.lang = 'en'
        else:
            self.lang = 'cs'

        self.selected_tags = self.tags[0][self.lang]
        self.doc_path = self.doc_path + self.lang + '/'

        self.run = run

        with open(topics_path, "r") as f:
            self.topics = f.read()


    def parse_docs_parallel(self):
        print('Parse and index documents')
        with Pool() as pool:
            result  = list(tqdm(pool.imap(self.parse_documents, self.doc_list)))
        if result:
            self.parsed_docs = pd.DataFrame.from_records(self.parsed_doc_list)
        

    def parse_documents(self, doc):
        full_doc_path = self.doc_path + doc
        with open(full_doc_path, "r") as f:
            xml_doc = f.read()
            parsed_doc = BeautifulSoup(xml_doc, 'lxml')
            all_docs = parsed_doc.findAll('doc')
            for doc in all_docs:
                doc_id = doc.find('docid').text
                relevant_text = doc.findAll(self.is_tag_included)
                doc_content = ' '.join([relevant_text[i].text for i in range(
                    len(relevant_text)) if relevant_text[i].text != ''])
                doc_dict = {'docno': doc_id, 'text': ' '.join(self.preprocess.preprocess(doc_content, self.lang, self.run))}
                self.parsed_doc_list.append(doc_dict)
        return True

    def is_tag_included(self, tag):
        return tag.name.upper() in self.selected_tags

    def create_queries(self):
        topic_list = re.findall(r'<num>(.+?)</num>', self.topics)
        self.topics = re.findall(r'<title>(.+?)</title>', self.topics)
        self.topic_title_map = [{
            'qid': topic_list[i], 'query': ' '.join(self.preprocess.preprocess(self.topics[i], self.lang, self.run))} for i in range(len(topic_list))]
        self.query_df = pd.DataFrame.from_records(self.topic_title_map)


    def get_output(self, result, output_file, run):
        with open(output_file, "w") as f:
            for index, row in result.iterrows():
                output_string = row['qid'] + '\t0\t' + row['docno'] + '\t' + \
                    str(row['rank']) + '\t' + str(row['score']) + '\t' + run + '\n'
                f.write(output_string)
