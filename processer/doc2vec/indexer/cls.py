from collections import defaultdict
import math
import numpy as np


def WeightMap():
    return defaultdict(lambda: 0)

class Indexer:
    def __init__(self, tokenaizer, vectaizer, sentimentAnalyzer) -> None:
        self._tokenaizer = tokenaizer
        self._vectaizer = vectaizer
        self._sentimentAnalyzer = sentimentAnalyzer 
        
    def exec(self, text:str):

        nodes = []
        count = 0
        key_map:defaultdict[str, int] = WeightMap()


        for subnodes, line in self._tokenaizer.exec(text):
            subcount = len(subnodes)
            
            sublen = subcount - int(subcount > 1 )       
            scored_subnodes = [ (face, 1 - math.sin(math.pi * position / sublen ) * 0.8  - 0.1 * position / sublen,) for face, position in subnodes]
            nodes.append((scored_subnodes, count, line, ))
            count += 1
        nodeslen  = count - int(count > 1)
    
       
        for subnodes, position, line in nodes:
           
            #weights:defaultdict 
            weights, positionWeight = self._computeWait(subnodes, position, nodeslen)
            self._processSentiment(line, weights, positionWeight)
        
            for k, v in weights.items():
                key_map[k] += v


        
        total = sum(key_map.values())
        reguraised = {k:v / total for k, v in key_map.items()}
        vector_map:dict[str, np.ndarray] =  self._vectaizer.exec_dict(key_map.keys())
        vector = np.sum([vector_map[k] * w for k, w in  reguraised.items() if vector_map[k] != False], 0)
        sentimentResults = self._processSentiTotal(vector_map, vector)
        word_index = list(vector_map.keys())
        norms = np.linalg.norm(np.array(vector_map.values()) - vector, axis=1)
        avg = np.average(norms)
        #std = np.std(norms)
        sorted_array = np.argsort(norms)
        scored_keywords:list[str] = [word_index[i] for i in sorted_array if norms[i] < avg]

        return vector, sentimentResults,scored_keywords 


    def _processSentiTotal(self, vectorMap, vector):
        sentimentVecrors = {}
        for sentiment, sentimentWords in self._sentimentWordMap.items():
            total = sum(sentimentWords.values())
            if total == 0:
                continue 
            reguraised = {k:v / total for k, v in sentimentWords.items()}
            sentimentVecrors[sentiment] = sum([vectorMap(k) * w for k, w in  reguraised.items()])
        total = sum(self._sentimentRatio.values())
        sentimentWeights = {sentiment:weight / total for sentiment, weight in self._sentimentRatio.items() }
        return sentimentVecrors, sentimentWeights


            
    def _initSentimentMap(self):
        negative = WeightMap()
        positive = WeightMap()
        neutral = WeightMap()

        self._sentimentWordMap = dict(negative=negative, positive=positive, neutral=neutral)
        self._sentimentRatio = WeightMap()
    def _processSentiment(self, line:str, weigts:defaultdict, positionWeight:float):
        sentiments = self._analizeSentiment(line)
        for face, weight in weigts.items():
            for sentiment, sWeight in sentiments:
                self._sentimentWordMap[sentiment][face] += weight * sWeight * positionWeight
        for sentiment, sWeight in sentiments:
            self._sentimentRatio[sentiment] += sWeight * positionWeight

            



    def _analizeSentiment(self, line):
        return self._sentimentAnalyzer.exec(line)

    def _computeWait(self, subnodes, position, nodeslen):
        weights = WeightMap()
        nodeWeight = 1 -  math.sin(math.pi * position / nodeslen) * 0.6 - 0.1 * position / nodeslen
        for surface, subscore in subnodes:
            weights[surface] += subscore * nodeWeight
        return weights, nodeWeight

