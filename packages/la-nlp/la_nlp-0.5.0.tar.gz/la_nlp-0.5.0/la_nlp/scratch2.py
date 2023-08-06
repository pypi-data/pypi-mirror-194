from la_nlp.pipes import aspect_sentiment as asp
import spacy

text = "Professor Doe was a very passionate lecturer, but I did not enjoy taking this course."

doc = asp.make_doc(text, parent_span_min_length=3)

for kw in doc._.keywords:
    print(kw, kw._.parent_span)

print('------------------------')

for token in doc:
    print(token, token.pos_, token.dep_)
