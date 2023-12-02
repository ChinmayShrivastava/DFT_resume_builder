from langchain.embeddings import OpenAIEmbeddings
import os
import json
from dotenv import load_dotenv
load_dotenv()

embeddings_model = OpenAIEmbeddings(openai_api_key=os.environ.get('OPENAI_API_KEY'))

def get_embedding(chunks: list, embeddings_model=embeddings_model, batch_size=10):
    embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        embeddings_ = embeddings_model.embed_documents(batch)
        embeddings.extend(embeddings_)
        print(f"Finished embedding {i} to {i+batch_size} out of {len(chunks)}")
    return chunks, embeddings

def open_data_json():
    # list all the .json files available in the data/ directory
    # ask the user to select one
    # open the selected file
    for filename in os.listdir('data'):
        if filename.endswith('.json'):
            print(filename)
    filename = input('Enter filename: ')
    if filename:
        with open(f'data/{filename}', 'r') as f:
            data = json.load(f)
    else:
        print("No filename entered. Using default data.json")
        with open('data/data.json', 'r') as f:
            data = json.load(f)
    # with open('data/data.json', 'r') as f:
    #     data = json.load(f)
    return data

def save_embeddings(data):
    embeddings_json = {}
    for i, element in enumerate(data):
        print(f"Saving embeddings for element {i}")
        edu_embeddings = get_embedding(data[element]["edu_chunks"])[1]
        exp_embeddings = get_embedding(data[element]["exp_chunks"])[1]
        for j, edu_embedding in enumerate(edu_embeddings):
            embeddings_json[f"{i}_edu_{j}"] = edu_embedding
        for j, exp_embedding in enumerate(exp_embeddings):
            embeddings_json[f"{i}_exp_{j}"] = exp_embedding
    with open('data/embeddings.json', 'w') as f:
        json.dump(embeddings_json, f, indent=4)

def embed_pipeline():
    data = open_data_json()
    save_embeddings(data)

# if __name__ == '__main__':
#     data = open_data_json()
#     save_embeddings(data)