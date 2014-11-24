import os
import nltk.data
import xml.etree.ElementTree as ET
import math

from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()


def verbAndConceptFreq(path):
    verb_freq_concept = {}

    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    for file in os.listdir(path):
        if file.startswith('.xml'):
            text = open(path + file).readlines()
            for line in text[1:]:#exclude first line of each file line since that is information about the file format.
                try:
                    sentences = sent_detector.tokenize(line.strip())
                except UnicodeDecodeError:
                    sentences = sent_detector.tokenize(line.strip().decode('utf-8'))
                for sentence in sentences:
                    if '<term' in sentence: 
                        try:
                            tags = nltk.pos_tag(nltk.word_tokenize(sentence))
                        except UnicodeDecodeError:
                            tags = nltk.pos_tag(nltk.word_tokenize(sentence.decode('utf-8')))
                        for tag in tags:
                            if tag[1].startswith('VB'):
                                #lemma = lmtzr.lemmatize(tag[0].lower()) #needs to have good lemmatizer eat, ate
                                if tag[0].lower() in verb_freq_concept:
                                    verb_freq_concept[tag[0].lower()] +=1
                                else:
                                    verb_freq_concept[tag[0].lower()] = 1
    return verb_freq_concept

def main():
    verb_freq = {}
   
    for line in open('verb_freq.txt').readlines():
        verb, freq = line.strip().split()
        verb_freq[verb] = freq
       
    #paths = ['craft-1.0/genia-xml/term/cl/', 'craft-1.0/genia-xml/term/so/', 'craft-1.0/genia-xml/term/pr/']
    paths = ['craft-1.0/genia-xml/term/t1/', 'craft-1.0/genia-xml/term/t/', 'craft-1.0/genia-xml/term/t2/']
    
    verb_freq_concepts = []
    verb_freq_concept = {}
    verb_posterior_dist = [] 

    prior = [0.055, 0.213, 0.151]

    for path in paths:
        verb_freq_concept = verbAndConceptFreq(path)
        verb_freq_concepts.append(verb_freq_concept)
    
    total_concepts = sum(len(i) for i in verb_freq_concepts)
    print 'total concepts: ', total_concepts
   
    for verb_concept in verb_freq_concepts:
        posterior = {}
        for t in verb_concept: #sorted(verb_freq_concepts[0].items(), key = lambda x:x[1], reverse=True): #sort verbs by their freq
            try:
                num = float(verb_concept[t])/total_concepts #frequency of a concept and a verb
                denum = float(verb_freq[t])/len(verb_freq) #frequence of a verb
                #print t[0], '\t', t[1], '\t', verb_freq[t[0]], '\t', num, '\t', denum, '\t', num/denum 
                posterior[t] = num/denum
            except KeyError:
                pass
        verb_posterior_dist.append(posterior)

    verb_concept_total_posterior = {}
    #Normalize
    for verb_concept in verb_posterior_dist:
        for verb in verb_concept:
            if verb in verb_concept_total_posterior:
                verb_concept_total_posterior[verb] += verb_concept[verb]
            else:
                verb_concept_total_posterior[verb] = verb_concept[verb]

    cnt = 0
    sps = {}
    for verb_concept in verb_posterior_dist:
        #print sorted(i.items(), key=lambda x:x[1], reverse=True)[:20]
        for verb in verb_concept:
            #print verb, '\t', verb_concept[verb], '\t', prior[cnt], '\t', verb_concept[verb]/prior[cnt], '\t', math.log(verb_concept[verb]/prior[cnt])
            norm = prior[cnt]/verb_concept_total_posterior[verb]
            if verb in sps:
                sps[verb] += (verb_concept[verb]* norm * (math.log(verb_concept[verb]*norm/prior[cnt])))
            else:
                sps[verb] = verb_concept[verb]*norm * (math.log(verb_concept[verb]*norm /prior[cnt]))
        cnt += 1 
    print sorted(sps.items(), key=lambda x:x[1], reverse=True)[:20]

if __name__=='__main__':
    main()
