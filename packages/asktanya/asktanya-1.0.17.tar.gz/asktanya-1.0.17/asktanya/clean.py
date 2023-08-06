import nltk

from nltk import pos_tag
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from string import punctuation

from collections import defaultdict
from nltk.corpus import stopwords


def clean_text(text):
    stop_words = set(
        stopwords.words("english")
        + list(punctuation)
        + ["''", "»", "‘", "‘", "’", "“", "”", "•", "■", "♦️"]
    )
    tag_map = defaultdict(lambda: wn.NOUN)
    tag_map["J"] = wn.ADJ
    tag_map["V"] = wn.VERB
    tag_map["R"] = wn.ADV
    tokens = nltk.word_tokenize(text)
    lemma_function = WordNetLemmatizer()
    lemmas = []
    for token, tag in pos_tag(tokens):
        item = lemma_function.lemmatize(token, tag_map[tag[0]])
        if item not in stop_words:
            lemmas.append(item)
    # lemmas= ' '.join(lemmas)
    return lemmas
