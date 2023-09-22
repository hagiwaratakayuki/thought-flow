import numpy as np
class SentimentWeights:
    neutral:float
    positive:float
    negative:float

class SentinmentVector:
    neutral:np.ndarray
    positive:np.ndarray
    negative:np.ndarray

class SentimentResult:
    vectors:SentinmentVector
    weights:SentimentWeights


    