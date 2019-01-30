from rank_bm25 import BM25Okapi, BM25L, BM25Plus
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from time import time

corpus = [
    "Hello there good man!",
    "It is quite windy in London",
    "How is the weather today?"
]
tokenized_corpus = [doc.split(" ") for doc in corpus]


def tokenizer(doc):
    doc = doc.lower()
    doc = re.sub(r"[^\w\s]+", "", doc)
    words = word_tokenize(doc)

    ps = PorterStemmer()
    return [ps.stem(w) for w in words]


def test_corpus_loading():

    algs = [
        BM25Okapi(tokenized_corpus),
        BM25L(tokenized_corpus),
        BM25Plus(tokenized_corpus)
    ]

    for alg in algs:
        assert alg.corpus_size == 3
        assert alg.avgdl == 5
        assert alg.doc_len == [4, 6, 5]


def test_tokenizer():
    bm25 = BM25Okapi(corpus, tokenizer=tokenizer)
    assert bm25.corpus_size == 3
    assert bm25.avgdl == 5
    assert bm25.doc_len == [4, 6, 5]


def test_tokenizer_speed():
    # Parsing 100k documents shouldn't take more than 5s
    t0 = time()
    BM25Okapi(corpus[:1]*100_000, tokenizer=tokenizer)
    t1 = time()
    exec_time = t1-t0
    assert exec_time < 5
