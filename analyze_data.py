import re
from collections import Counter
import pickle
with open('outfile', 'rb') as fp:
    itemlist = pickle.load(fp)
words_list = list()


for word in itemlist:
	if word == "":
		continue
	word = word.replace("(", "")
	word = word.replace(")", "")
	words_list.append(word.lower())
print Counter(words_list).most_common()
