import spacy

from la_nlp.pipes import aspect_sentiment as asp
from la_nlp import utils

aspects = {'tests':['mid-term', 'mid term']}
keywords = utils.get_keywords_from_aspects(aspects)

nlp = spacy.load('en_core_web_lg')

rules = nlp.tokenizer.rules
rules['mid-term'] = [{65: 'mid-term'}]
rules['mid-terms'] = [{65: 'mid-terms'}]
rules['mid term'] = [{65: 'mid term'}]
nlp.tokenizer.rules = rules

text = "I wish the mid terms mid-terms had included more questions about world history."

doc = nlp(text)

doc = asp.aspect_sentiment_pipe(doc, aspects, keywords)

for kw in doc._.keywords:
    print(kw.lemma_)
