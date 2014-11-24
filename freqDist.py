
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

text = open('all').readlines()

fdist = FreqDist()
for line in text:
    if line != '\n':
        try:
            for word in word_tokenize(line.strip()):
                fdist[word.lower()] += 1
        except UnicodeDecodeError:
            for word in word_tokenize(line.strip().decode('utf-8')):
                fdist[word.lower()] += 1
print fdist.most_common(10) 
