import os
import json
from embed import get_embedding
import numpy as np

# open data.json
def open_data_json():
    with open('data/data.json', 'r') as f:
        data = json.load(f)
    return data

# open embeddings.json
def open_embeddings_json():
    with open('data/embeddings.json', 'r') as f:
        embeddings = json.load(f)
    return embeddings

datajson = open_data_json()
embeddings = open_embeddings_json()

def vector_search(query, embeddings=embeddings, datajson=datajson):
    vector = get_embedding([query])[1][0]
    results = []
    for key in embeddings:
        result = {}
        result["key"] = key
        result["score"] = cosine_similarity(vector, embeddings[key])
        results.append(result)
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    # for each key in results, get the corresponding data
    for result in results:
        key = result["key"]
        key_split = key.split("_")
        index = int(key_split[0])
        edu_or_exp = key_split[1]
        edu_or_exp_index = int(key_split[2])
        result["data"] = datajson[f'{index}'][f"{edu_or_exp}_chunks"][edu_or_exp_index]
    print(results[0]["data"])
    return results

def cosine_similarity(vector1, vector2):
    return np.dot(vector1, vector2)/(np.linalg.norm(vector1)*np.linalg.norm(vector2))

if __name__ == '__main__':
    query = "consulting delloitte"
    results = vector_search(query)
    # print(results)