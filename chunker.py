import os
import json

# open all files from the data/ directory, and collect the data, return a list
def open_files():
    files = []
    for filename in os.listdir('data'):
        if filename.endswith('.txt'):
            with open('data/' + filename, 'r') as f:
                files.append(f.read())
    return files

# for each file, split by ~ and return a list of lists
def split_files(files):
    split_files = []
    for file in files:
        split_files.extend(file.split('!@#'))
    return split_files

# for each passed split file, extract education and experience by splitting by double #
def extract_education_and_experience(split_files):
    education_experience = []
    for file in split_files:
        split_file = file.split('##')
        education_experience.append(split_file)
    return education_experience

def final_chunks(edu_exp_element):
    education = edu_exp_element[0]
    experience = edu_exp_element[1]
    education_chunks = education.split('#')
    experience_chunks = experience.split('#')
    return education_chunks, experience_chunks

def embed

if __name__ == '__main__':
    files = open_files()
    split_files = split_files(files)
    education_experience = extract_education_and_experience(split_files)
    [print(x) for x in education_experience[0:2]]