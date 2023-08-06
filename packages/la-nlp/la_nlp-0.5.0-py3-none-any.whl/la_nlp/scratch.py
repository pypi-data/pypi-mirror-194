from la_nlp.pipes import aspect_sentiment as asp

text = "Professor Doe is a great instructor."

TEST_TEXT_4 = (
    "Professor Doe was a very passionate lecturer who presented "
    "the material quite differently from other courses I have taken. The "
    "only 'problem' I had with his course was how much bias and personal "
    "opinion they interjected in their lectures. A lot of the material "
    "presented was really just opinion and we spent too much time on that, "
    "which did not effectively facilitate learning of the subject matter. "
    "The extra material they brought in, however, was quite interesting and "
    "helped provide deeper understanding of certain subjects."
)

doc = asp.make_doc(TEST_TEXT_4, anonymize=True)

for token in doc:
    print(token, token.ent_type_)