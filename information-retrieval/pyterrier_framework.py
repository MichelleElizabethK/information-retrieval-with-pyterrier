import pyterrier as pt
import pyterrier_doc2query
import pandas as pd
import subprocess
from config import config
from pyterrier_t5 import MonoT5ReRanker


class PythonTerrier:
  def __init__(self, doc_df, lang, run):
    if not pt.started():
      pt.init(boot_packages=['com.github.terrierteam:terrier-prf:-SNAPSHOT'])
    self.docs_df = doc_df
    self.index = None
    self.lang = lang
    self.run = run

  def index_docs(self):
    remove_idx_command = 'rm -rf ./index'
    process = subprocess.Popen(remove_idx_command.split(), stdout=subprocess.PIPE)
    process.communicate()
    tokeniser = config[self.lang][self.run]['tokeniser']
    index_type = pt.index.IndexingType.CLASSIC if config[self.lang][self.run]['indexing_type'] == 1 else pt.index.IndexingType.SINGLEPASS

    if self.lang == 'en':
      stemmer = 'porter' if config[self.lang][self.run]['stemming'] else None
      stopwords = 'terrier' if config[self.lang][self.run]['remove_stopwords'] else None
    else:
      stemmer = None
      stopwords = None    

    indexer = pt.IterDictIndexer("./index", type=index_type, stemmer=stemmer, stopwords=stopwords, tokeniser=tokeniser, verbose=True, meta= {'docno' : 26, 'text' : 2048},)
    if config[self.lang][self.run]['doc2query']:
      doc2query = pyterrier_doc2query.Doc2Query(append=True, verbose=True) 
      indexer = doc2query >> indexer
    self.index = indexer.index(self.docs_df.to_dict(orient='records'))


  def query_docs(self, topics):
    monoT5 = MonoT5ReRanker()
    controls = {}
    # Experiment with collection enrichment/external feedback using wikipedia index
    # remove_idx_command = 'rm -rf ./wiki_index'
    # process = subprocess.Popen(remove_idx_command.split(), stdout=subprocess.PIPE)
    # process.communicate()
    # wiki_index = pt.IterDictIndexer("./wiki_index").index(pt.get_dataset("irds:wikiclir/en-simple").get_corpus_iter())
    controls['wmodel'] = config[self.lang][self.run]['weighting_model']
    wm = pt.BatchRetrieve(self.index, wmodel=controls['wmodel'], num_results=1000)
    # pipe = wm >> pt.rewrite.stash_results() >> pt.BatchRetrieve('./wiki_index') >> pt.rewrite.RM3('./wiki_index') >> pt.rewrite.reset_results() >> wm
    # result = pipe.transform(topics)
    pipe = wm

    if config[self.lang][self.run]['doc2query']:
      doc2query = pyterrier_doc2query.Doc2Query(verbose=True)
      pipe = pipe >> doc2query

    if config[self.lang][self.run]['query_expansion']:
      qemodel = config[self.lang][self.run]['query_expansion']

      # if(qemodel != qemodels[0]):
      #   pipe = pipe >> pt.rewrite.stash_results()

      if qemodel in ['Bo1', 'Bo2', 'BA']:
        controls['qe'] = 'on'
        controls['qemodel'] = qemodel
        wm = pt.BatchRetrieve(self.index, controls = controls, verbose=True, num_results=1000)
        pipe = wm
      elif qemodel == 'RM3':
        qe = pt.rewrite.RM3(self.index)
      elif qemodel == 'AxiomaticQE':
        qe = pt.rewrite.AxiomaticQE(self.index)
      elif qemodel == 'KL':
        qe = pt.rewrite.KLQueryExpansion(self.index)

        pipe = pipe >> qe
    
      if config[self.lang][self.run]['doc2query']:
        pipe = pipe >> pt.text.scorer(body_attr="querygen", wmodel=controls['wmodel'])
      else:
        # pipe = pipe >> pt.rewrite.reset_results() >> wm
        # if qemodel not in ['Bo1', 'Bo2', 'BA']:
        if self.lang == 'en':
          pipe = pipe >> pt.text.get_text(self.index, 'text') >> monoT5


        result = pipe.transform(topics)
    else:
      result = pt.BatchRetrieve(self.index, controls = controls, verbose=True, num_results=1000).transform(topics)
    return result