
import nltk



FILTERS = ['NN', 'NNS', 'NNP', 'NNPS']

FILTERS_MAP = dict(zip(FILTERS, [True] * len(FILTERS)))

class NLTKTokenazer:
    def exec(self, text:str):
        results = []
        for line in text.splitlines():
            tokens = nltk.word_tokenize(line)
            tags = nltk.pos_tag(tokens)
            
            results.extend(([face for face, tag in tags if tag in FILTERS_MAP], line,))
        return results


