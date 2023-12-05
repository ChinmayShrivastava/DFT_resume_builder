import os
import json
from search import *
from prompts import COMPARE_RESUME
from openai import OpenAI

client = OpenAI()

def generate_completion(prompt):
    # response = client.completions.create(
    #     engine="davinci",
    #     prompt=prompt,
    #     max_tokens=150,
    #     temperature=0.9,
    #     top_p=1,
    #     frequency_penalty=0.0,
    #     presence_penalty=0.0,
    #     stop=["\n", "Human:", "AI:"]
    # )
    # return response
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=1000,
    temperature=1,
    stream=True
    )
    for message in response:
        if message.choices[0].delta.content is not None:
            # print(message.choices[0].delta.content)
            yield message.choices[0].delta.content

def open_data_json(filename=None):
    with open(f'data/{filename}.json', 'r') as f:
        data = json.load(f)
    return data

# open embeddings.json
def open_embeddings_json(filename=None):
    with open(f'data/{filename}.json', 'r') as f:
        embeddings = json.load(f)
    return embeddings

class Resume():

    def __init__(self, job_description, resume_experience):
        self.job_description = job_description
        self.resume_experience = resume_experience
        self.data = open_data_json('general0')
        self.embeddings = open_embeddings_json('general0_embeddings')
        self.fs_prompt = "Based on the job description and notes, explain step-by-step how to write the resume's experience section and then output the resume's experience section as illustrated in some examples before.\n"
        self.resume_updated = ''
        self.resume_explanation = None
        self.results = None

    def perform_similarity_search(self):
        self.results = vector_search(self.job_description, self.embeddings, self.data)[0:3]
        i = 0
        for result in self.results:
            self.fs_prompt += f"{i+1}. {result} \n"
        self.fs_prompt += f"Job Description: {self.job_description}\nNotes: {self.resume_experience}"

    def resume_generator(self, placeholder):
        generator = generate_completion(self.fs_prompt)
        for message in generator:
            self.resume_updated+=message
            formatted_message = self.resume_updated.replace('\n', '<br>')
            placeholder.markdown(f'<pre>{formatted_message}</pre>', unsafe_allow_html=True)