from doc2vec.vectaizer.gensim_fasttext import loadVectors

vec = loadVectors()
count = 0
for k in vec.key_to_index:
    print(type(k))
    count +=1 
    if count > 100:
        break