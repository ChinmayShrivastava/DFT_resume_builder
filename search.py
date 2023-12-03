import os
import json
from embed import get_embedding
import numpy as np

# open data.json
# def open_data_json():
#     with open('data/data.json', 'r') as f:
#         data = json.load(f)
#     return data

# def open_data_json():
#     # list all the .json files available in the data/ directory
#     # ask the user to select one
#     # open the selected file
#     for filename in os.listdir('data'):
#         if filename.endswith('.json'):
#             print(filename)
#     filename = input('Enter filename: ')
#     if filename:
#         with open(f'data/{filename}', 'r') as f:
#             data = json.load(f)
#     else:
#         print("No filename entered. Using default data.json")
#         filename = 'data.json'
#         with open('data/data.json', 'r') as f:
#             data = json.load(f)
#     # with open('data/data.json', 'r') as f:
#     #     data = json.load(f)
#     return data, filename

# # open embeddings.json
# def open_embeddings_json():
#     for filename in os.listdir('data'):
#         if filename.endswith('.json'):
#             print(filename)
#     filename = input('Enter filename: ')
#     if filename:
#         with open(f'data/{filename}', 'r') as f:
#             embeddings = json.load(f)
#     else:
#         print("No filename entered. Using default embeddings.json")
#         filename = 'embeddings.json'
#         with open('data/embeddings.json', 'r') as f:
#             embeddings = json.load(f)
#     # with open('data/embeddings.json', 'r') as f:
#     #     embeddings = json.load(f)
#     return embeddings

# datajson = open_data_json()[0]
# embeddings = open_embeddings_json()

def vector_search(query, embeddings, datajson):
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
        result["data"] = datajson[f"{index}"]["fewshot_prompt"]
    return [result['data'] for result in results]

def cosine_similarity(vector1, vector2):
    return np.dot(vector1, vector2)/(np.linalg.norm(vector1)*np.linalg.norm(vector2))

# if __name__ == '__main__':
#     query = "consulting delloitte"
#     results = vector_search(query)
#     print(results)