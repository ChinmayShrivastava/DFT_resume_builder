from agents import *
import os
import json
from prompts import COT_GEN_PROMPT
import time
from dotenv import load_dotenv
load_dotenv()

AGENT_ID = os.environ.get('AGENT_ID')

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
        filename = 'data.json'
        with open('data/data.json', 'r') as f:
            data = json.load(f)
    # with open('data/data.json', 'r') as f:
    #     data = json.load(f)
    return data, filename

def create_cot(data):
    for i in data:
        education_text = ''
        data[i]['exp_chunks_mod'] = [None] * len(data[i]['exp_chunks'])
        for j in range(len(data[i]['edu_chunks'])):
            i_ = f'{i}'
            j_ = int(j)
            education_text += f'{data[i_]["edu_chunks"][j_]}\n'
        prompt_pre = COT_GEN_PROMPT.replace('<<EDUCATION>>', education_text)
        for j in range(len(data[i]['exp_chunks'])):
            message = {
                "role": "user",
                "content": prompt_pre.replace('<<ENTRY>>', data[i]['exp_chunks'][int(j)])
            }
            threadid = create_thread([message]).id
            runid = run_assistant(AGENT_ID, threadid).id
            while True:
                time.sleep(2)
                run = get_run(runid, threadid)
                if run.status == 'completed':
                    break
            response = get_response(threadid)
            last_message = response.data[0].content[0].text.value
            data[i]['exp_chunks_mod'][j] = last_message
            print(last_message)

def cot_pipeline():
    data, filename = open_data_json()
    create_cot(data)
    with open(f'data/{filename}', 'w') as f:
        json.dump(data, f, indent=4)

# if __name__ == '__main__':
#     data, filename = open_data_json()
#     create_cot(data)
#     with open(f'data/{data}', 'w') as f:
#         json.dump(data, f, indent=4)