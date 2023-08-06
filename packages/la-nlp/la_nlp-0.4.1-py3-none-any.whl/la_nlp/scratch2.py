from la_nlp.pipes import aspect_sentiment as asp
import spacy

text = """
The food was delicious, but the service was terrible.
"""

aspects = {
    'Food':['food'],
    'Service':['service']
}

doc = asp.make_doc(text, aspects=aspects, parent_span_min_length=7)

for kw in doc._.keywords:
    print(kw.text, '-', kw._.parent_span, '-', kw in kw._.parent_span)

print(doc._.aspect_sentiments)
