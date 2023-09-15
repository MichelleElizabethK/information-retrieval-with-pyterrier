config = {
    "en": {
        "run-0": {
            "lowercase": False,
            "stemming": False,
            "lemmatize": False,
            "remove_stopwords": False,
            "tokeniser": 'WhitespaceTokeniser',
            "indexing_type": 1,
            "weighting_model": "Tf",
            "query_expansion": None,
            "doc2query": False
        },
        "run-1": {
            "lowercase": True,
            "stemming": True,
            "lemmatize": False,
            "remove_stopwords": True,
            "tokeniser": 'EnglishTokeniser',
            "indexing_type": 1,
            "weighting_model": "BB2",
            "query_expansion": 'Bo2',
            "doc2query": False
        }
    },
    "cs": {
        "run-0": {
            "lowercase": False,
            "stemming": False,
            "lemmatize": False,
            "remove_stopwords": False,
            "tokeniser": 'WhitespaceTokeniser',
            "indexing_type": 1,
            "weighting_model": "Tf",
            "query_expansion": None,
            "doc2query": False
        },
        "run-1": {
            "lowercase": True,
            "stemming": False,
            "lemmatize": True,
            "remove_stopwords": True,
            "tokeniser": 'UTFTokeniser',
            "indexing_type": 1,
            "weighting_model": "DFRee",
            "query_expansion": 'BA',
            "doc2query": False
        }
    }
}
