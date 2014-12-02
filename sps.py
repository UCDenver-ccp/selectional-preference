import os
import nltk.data
import xml.etree.ElementTree as ET
import math

from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()


def verbAndConceptFreq(path):
    verbConceptFreq = {} #keys are verbs, values are occurrence of the verb for a given concept. concept is determined by the argument of the function.

    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    for file in os.listdir(path):
        if file.endswith('.xml'):
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
                                lemma = lmtzr.lemmatize(tag[0].lower(), 'v') #needs to have good lemmatizer eat, ate
                                if lemma in verbConceptFreq:
                                    verbConceptFreq[lemma] +=1
                                else:
                                    verbConceptFreq[lemma] = 1
    return verbConceptFreq 

def selectionalPreferenceStrength(prior, posterior):
    '''
    prior: list of priors. Order is important. It indicates order of concepts.
    posterior: dictionary. Keys are verbs and values are list of conditional probabilities. P(class_i|verb).
    '''
    sps = {}
    for verb in posterior:
        tmp = []
        for i in range(0, len(prior)):
            tmp += [posterior[verb][i]*math.log(posterior[verb][i]/prior[i], 2)] 
        sps[verb] = sum(tmp) #sum
    return sps

def selectionalAssociation(prior, posterior, sps):
    maxConcept = {}
    for verb in posterior:
        tmp = []
        for i in range(0, len(prior)):
            tmp += [posterior[verb][i]*math.log(posterior[verb][i]/prior[i], 2)]
        #print verb, tmp,
        try:
            sa = [i*1/(sps[verb]) for i in tmp]
            #print sa
            m = max(sa)
            maxConcept[verb] = [i for i, j in enumerate(sa) if j == m]
        except ZeroDivisionError:
            #print 'selectional association for this verb is zeror.'    
            pass
    return maxConcept

def main():
    verbFreq = {}
    verbConceptFreqTotal = {}
    verbPosterior = {}
    #####################################################Testing selectional preference strength.
    prior = [0.25, 0.25, 0.25, 0.25]
    pos = {}
    pos['eat'] = [0.01, 0.01, 0.97, 0.01]
    pos['see'] = [0.25, 0.25, 0.25, 0.25]
    pos['find'] = [0.33, 0.33,0.33, 0.01]
    
    sps = selectionalPreferenceStrength(prior, pos)
    ######################################################


    #####################################################Testing selectional association.
    sa = selectionalAssociation(prior, pos, sps) 
    concepts = ['people', 'furniture', 'food', 'action']
    ######################################################

    for line in open('verb_freq.txt').readlines():
        verb, freq = line.strip().split()
        verbFreq[verb] = freq

    #semantic concepts are in this list.   
    #paths = ['craft-1.0/genia-xml/term/chebi/','craft-1.0/genia-xml/term/cl/', \
    #       'craft-1.0/genia-xml/term/entrezgene/','craft-1.0/genia-xml/term/go_bpmf/',\
    #      'craft-1.0/genia-xml/term/go_cc/', 'craft-1.0/genia-xml/term/ncbitaxon/', \
    #       'craft-1.0/genia-xml/term/pr/', 'craft-1.0/genia-xml/term/so/']
    paths = ['./craft-1.0/genia-xml/term/t1/', 'craft-1.0/genia-xml/term/t2/', 'craft-1.0/genia-xml/term/t3/']
    

    '''
    This code will populate verbConceptFreqTotal{}
    verb_1 [occurrence of sc1, occurrence of sc2, occurrence of sc3, ... occurrence of sc8
    verb_2 [occurrence of sc1, occurrence of sc2, occurrence of sc3, ... occurrence of sc8
    verb_3 [occurrence of sc1, occurrence of sc2, occurrence of sc3, ... occurrence of sc8

    ....

    verb_N [occurrence of sc1, occurrence of sc2, occurrence of sc3, ... occurrence of sc8
    verbs are read from a dictionary stored in the file verb_freq.txt
    sc stands for semantic concept.
    '''
    for path in paths:#for each concepts. There are 8 concpets. these are indicated by values of the list paths.
        verbConceptFreq= verbAndConceptFreq(path)#this method returns verbs and their frequency in each concept. 
        for v in verbFreq:#do verbConceptFreq for all verbs and all concepts.
            if v not in verbConceptFreqTotal.keys(): #add new keys to dict.
                verbConceptFreqTotal[v] = []
            if v in verbConceptFreq:
                verbConceptFreqTotal[v].append(verbConceptFreq[v])
            else:
                verbConceptFreqTotal[v].append(0.00001)#add small value for verbs that don't co-occure with a concept for smoothing purpose.
    
    #prior = [0.079, 0.055, 0.119, 0.226, 0.080, 0.076, 0.151, 0.213]
    prior = [0.1, 0.3, 0.3]
    post = {}

    '''
    Compute conditional probability:
        P(concept_c | verb_v)  =  P(concept_c and verb_v)/P(verb_v)
    Numerator: Given a verb, what is the probability of a concept_c.
        Basically, marginalize verbConceptFreqTotal[verb] over concepts. 
        example: verbConceptFreqTotal['express'] = [1,2,3,4,5,6,7,8]
        P(concept_c| verb='express'] = [1,2,3,4,5,6,7,8]/36
    Denominator: count of verb_v in the corpus divide by total verbs. Basically frequency of a verb.
    '''
    for verb in verbConceptFreqTotal:
        verbConceptFreqTotal[verb] = [float(i)/sum(verbConceptFreqTotal[verb]) for i in verbConceptFreqTotal[verb]]#Normalize e.g. [1,2,3,4,5,6,7,8]/36
        #print verb, verbConceptFreqTotal[verb], 
        num = verbConceptFreqTotal[verb]#[1,2,3,4,5,6,7,8]/36
        denum = float(verbFreq[verb])/sum(int(i) for i in verbFreq.values())#P(verb_v])
        post[verb] = [i/denum for i in num] #computes conditonal probability for each concept given a verb i.e. P(concept_c | verb_v)  =  P(concept_c and verb_v)/P(verb_v)
        post[verb] = [i/sum(post[verb]) for i in post[verb]] #Normalize again.
    for v in post:
        print v, post[verb]

    #sps = selectionalPreferenceStrength(prior, post)
    '''
    for verb in sps:
        print verb, '\t', sps[verb]
    '''
    '''
    selectional association takes arguments
        prior, posterior, sps

    '''
    '''
    concepts = ['chebi', 'cl', 'entrezgene', 'go_bpmf', 'go_cc', 'ncbitaxon', 'pr', 'so']
    sa = selectionalAssociation(prior, post, sps)
    for v in sa:
        print v, '\t', 
        print [concepts[i] for i in sa[v]]
    '''
if __name__=='__main__':
    main()
