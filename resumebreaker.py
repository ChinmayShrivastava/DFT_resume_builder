import json
import os
from agents import *
import time
from dotenv import load_dotenv
load_dotenv()

AGENT_ID = os.environ.get('AGENT_ID2')

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

def informalize_resume(data):
    # temp_prompt = ''
    # for each entry in the data.json file
    for i in data:
        # for each chunk in the experience section
        temp_prompt = '\n'.join(data[i]['exp_chunks'])
        message = {
            "role": "user",
            "content": temp_prompt
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
        data[i]['notes'] = last_message
        print(last_message)

def informalize_pipeline():
    data, filename = open_data_json()
    informalize_resume(data)
    with open(f'data/{filename}', 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    informalize_pipeline()