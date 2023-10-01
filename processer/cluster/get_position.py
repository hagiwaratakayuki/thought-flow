from doc2vec.indexer.dto import SentimentResult
import numpy as np


def get_position(index2sentiments:dict[int, SentimentResult], cluster_members:frozenset):
    sumed_vecter = None
    not_init = True
    member_count = 0    
    index2directionvector = {}
    shape = [0, 0]
    for member in cluster_members:
        
        sentiment = index2sentiments[member]
        if not_init:
            sumed_vecter = np.zeros(sentiment.vectors.neutral.shape)
            shape[1] = sentiment.vectors.neutral.shape[0]
            not_init = False
        sumed_vecter += sentiment.vectors.neutral
        vector4direction = sentiment.vectors.positive - sentiment.vectors.negative
        
        direction_norm = np.linalg.norm(vector4direction.shape)
        if direction_norm == 0:
            direction_norm = 1
       
        index2directionvector[member_count] = vector4direction / direction_norm
        
        member_count += 1
    center_vecter = sumed_vecter / member_count  # type: ignore type length 4
    reguraized_center_vecter = sumed_vecter / (np.linalg.norm(sumed_vecter) or 1)  # type: ignore length 4
    shape[0] = member_count
    vecters4direction = np.zeros(shape=shape)
    vecters4position = np.zeros(shape=shape)
    
    for index in range(member_count):
       
        vecters4direction[index] = index2directionvector[index]
        vecters4position[index] = index2sentiments[index].vectors.neutral
    directions = np.dot(vecters4direction, reguraized_center_vecter)
    directions[directions >= 0]  = 1
    directions[directions < 0] = -1
    non_regued_distances = np.linalg.norm(vecters4position - center_vecter, axis=1)
    max_distance = np.nanmax(non_regued_distances)  
    distances = (non_regued_distances / (max_distance or 1)) * directions
    return distances










