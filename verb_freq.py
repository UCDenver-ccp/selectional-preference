
import os
import nltk.data

from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

def getVerbFrequency(path):
    verb_freq = {}
    for file in os.listdir(path):
        if file.endswith('.txt'):
            text = open(path + file).readlines()
            for line in text:
                try:
                    sentences = sent_detector.tokenize(line.strip())
                except UnicodeDecodeError:
                    sentences = sent_detector.tokenize(line.strip().decode('utf-8'))
                for sent in sentences:
                    try:
                        tags = nltk.pos_tag(nltk.word_tokenize(sent))
                    except UnicodeDecodeError:
                        tags = nltk.pos_tag(nltk.word_tokenize(sent.decode('utf-8')))
                    for tag in tags:
                        if tag[1].startswith('VB'):
                            lemma = lmtzr.lemmatize(tag[0].lower(), 'v')
                            if lemma in verb_freq:
                                verb_freq[lemma] += 1
                            else:
                                verb_freq[lemma] = 1
    return verb_freq

def main():
    fileout  = open('./verb_freq.txt', 'w')
    path = 'craft-1.0/articles/txt/'
    verb_freq = getVerbFrequency(path) 

    for k in verb_freq:
       try:
           fileout.write(k)
       except UnicodeEncodeError:
           fileout.write(k.encode('utf-8'))
       fileout.write('\t') 
       fileout.write(str(verb_freq[k]))
       fileout.write('\n') 

if __name__ == '__main__':
    main()

