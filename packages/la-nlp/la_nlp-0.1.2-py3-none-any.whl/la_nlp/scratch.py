TEST_TEXT_3 = """
The class was good. I liked the course.
"""

from la_nlp.pipes import aspect_sentiment as asp

doc = asp.make_doc(TEST_TEXT_3)

for token in doc._.keywords:
    print(token.i, token, token._.parent_span._.sentiment)
