import re

kws = ['mid term', 'mid-term', 'mid/term', "mid'term"]

regex = "[-\s/']"

for kw in kws:
    print(kw, re.search(regex, kw))
