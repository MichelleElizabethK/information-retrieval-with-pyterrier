# Information Retrieval System Using PyTerrier Framework

This project uses the PyTerrier framework to develop an information retireval system for English and Czech datasets.

## Model Specifications

#### English

- token delimiters: EnglishTokeniser from PyTerrier
- term equivalence classes: stemming
- removing stopwords: True
- query construction: all words from topic "title"
- weighting: BB2
- pseudo-relevance feedback: True
- query expansion: Bo2
- reranking algorithm: MonoT5

Mean average precision = 0.4226


#### Czech

- token delimiters: UTFTokeniser from PyTerrier
- term equivalence classes: lemmatisation
- removing stopwords: True
- query construction: all words from topic "title"
- weighting: DFRee
- pseudo-relevance feedback: True
- query expansion: BA
- reranking algorithm: None

Mean average precision = 0.3448

## How To Run the System

The Python version used is 3.8.16

First create a virtual env, activate it and install the requirements:

`
python -m venv venv
`

`
source venv/bin/activate
`

`
pip install -r requirements.txt
`

On the terminal, run the following command from the root directory:

`
python information-retrieval/run.py -q <topics.xml> -d <documents.lst> -r <run-0 or run-1> -o <outputfile.res>
`
The configuration can be changed in the information-retrieval/config.py file.