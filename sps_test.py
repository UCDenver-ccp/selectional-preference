import unittest

from sps import selectionalPreferenceStrength
from sps import verbAndConceptFreq

class TestSelectionPreference(unittest.TestCase):
    def test_sps(self):
        
        prior = [0.25, 0.25, 0.25, 0.25]
        pos = {}

        pos['eat'] = [0.01, 0.01, 0.97, 0.01]
        pos['see'] = [0.25, 0.25, 0.25, 0.25]
        pos['find'] = [0.33, 0.33,0.33, 0.01]

        actual_sps = {}

        actual_sps['eat'] =  1.7580592671467892 
        actual_sps['see'] = 0.0
        actual_sps['find'] = 0.35009398839014433

        sps = selectionalPreferenceStrength(prior, pos)

        self.assertDictEqual(sps, actual_sps)
    def test_verbConceptFreq(self):
        paths = ['./craft-1.0/genia-xml/term/t1/', 'craft-1.0/genia-xml/term/t2/', 'craft-1.0/genia-xml/term/t3/']
        verbConceptFreq_actual = []
        
        verbConceptFreq_actual.append({'prevent': 1, 'compare': 4, 'have': 4, 'sequence': 1, 'contribute': 1, 'assess': 1, 'see': 1, 'identify': 1, 'determine': 1, 'follow': 1, 'help': 1, 'use': 1, 'thank': 1, 'support': 1, 'show': 2, u'increase': 5, u'analyze': 2, u'cause': 1, 'alter': 6, u'match': 1, u'do': 5, u'lack': 1, 'homozygous': 1, 'associate': 3, 'pigment': 3, 'demonstrate': 1, 'report': 1, 'be': 15, 'diabetes': 5, 'amplify': 1, 'decrease': 1, 'otherwise': 1})
        
        verbConceptFreq_actual.append({'prevent': 1, 'compare': 8, 'purify': 1, 'determine': 4, 'do': 8, 'fill': 1, 'house': 2, 'contribute': 3, 'focus': 1, 'assess': 1, 'strain': 4, 'interstrain': 1, u'identify': 8, u'expect': 1, 'have': 15, u'measure': 2, u'follow': 1, u'subject': 1, u'use': 5, u'develop': 1, 'thank': 1, u'decrease': 1, u'confirm': 1, 'provide': 1, 'suggest': 1, 'create': 1, u'sequence': 2, 'help': 1, u'publish': 1, 'degenerate': 1, u'increase': 7, u'call': 1, u'show': 3, u'include': 1, u'cause': 1, 'alter': 7, u'match': 1, u'be': 49, u'lack': 1, 'homozygous': 1, 'associate': 4, u'evaluate': 1, u'screen': 1, u'describe': 1, u'depend': 1, u'pigment': 5, u'backcross': 2, u'test': 1, u'train': 1, u'know': 3, u'report': 3, u'affect': 2, u'implicate': 1, 'diabetes': 6, u'analyze': 4, u'elevate': 1, u'study': 1, 'glaucoma': 1, 'mask': 1, 'see': 1, u'amplify': 1, '<': 28, u'allow': 4, u'become': 1, 'otherwise': 1, u'require': 1, u'result': 1})
        
        verbConceptFreq_actual.append({'show': 2, u'lack': 1, u'focus': 1, u'supplement': 1, u'identify': 1, u'follow': 3, u'compose': 1, '(': 1, u'add': 1, u'stain': 2, u'include': 3, '<': 5, u'do': 2, 'chromatin': 1, u'collaborate': 1, u'couple': 1, u'stop': 1, u'hybridize': 1, u'know': 1, u'affect': 2, u'reveal': 4, 'remove': 1, u'collect': 1, u'contain': 1, 'become': 1, 'unpublished': 2, u'resuspend': 1, u'culture': 2, u'result': 1, u'wonder': 1, u'detect': 1, u'label': 1, 'cause': 1, u'be': 41, 'run': 5, u'associate': 2, 'immunoprecipitated': 1, u'modify': 2, u'derive': 1, u'assemble': 1, u'generate': 1, u'study': 1, u'keep': 1, u'range': 1, 'transfected': 1, u'synthesize': 1, u'determine': 1, u'wrap': 1, 'next': 1, u'size': 1, u'use': 6, u'prepare': 3, u'interact': 2, u'mark': 1, u'indicate': 2, u'call': 1, u'treat': 1, u'analyze': 6, u'describe': 3, u'knockdown': 1, u'promote': 2, u'require': 2, u'recruit': 1, u'alter': 1, u'remain': 1, 'plasmid': 2, u'compare': 1, u'process': 1, u'contribute': 1, u'involve': 1, u'blot': 1, u'have': 1, u'lysed': 1, u'incubate': 3, u'conserve': 1, u')': 1, u'suggest': 1, u'whereas': 1, u'isolate': 2, u'ensure': 1, u'concern': 1, u'repeat': 1, u'plat': 1, 'reflect': 2, u'phase': 1, 'trypsinized': 1, u'purchase': 1, u'purify': 2, u'perform': 1, u'deposit': 2, u'allow': 1})

        for i in range(0, len(paths)):
            verbConceptFreq= verbAndConceptFreq(paths[i])#this method returns verbs and their frequency in each concept. 
            self.assertDictEqual(verbConceptFreq, verbConceptFreq_actual[i]) 
        '''
        verbConceptFreq= verbAndConceptFreq(paths[0])#this method returns verbs and their frequency in each concept. 
        self.assertDictEqual(verbConceptFreq, verbConceptFreq_actual[0]) 
        
        verbConceptFreq= verbAndConceptFreq(paths[1])#this method returns verbs and their frequency in each concept. 
        self.assertDictEqual(verbConceptFreq, verbConceptFreq_actual[1]) 
        
        verbConceptFreq= verbAndConceptFreq(paths[2])#this method returns verbs and their frequency in each concept. 
        self.assertDictEqual(verbConceptFreq, verbConceptFreq_actual[2]) '''

            #self.assertDictEqual(verbConceptFreq, verbConceptFreq_actual[1]) 
            #self.assertDictEqual(verbConceptFreq, verbConceptFreq_actual[2]) 

if __name__ == '__main__':
        unittest.main()

