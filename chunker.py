import os
import json
# from langchain.embeddings import OpenAIEmbeddings

# embeddings_model = OpenAIEmbeddings(openai_api_key="...")

# open all files from the data/ directory, and collect the data, return a list
def open_files(folder='data'):
    fol = input('Enter folder name: ')
    if fol:
        folder = fol
    files = []
    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            with open(f'{folder}' + filename, 'r') as f:
                files.append(f.read())
    return files

# for each file, split by ~ and return a list of lists
def split_files_into_chunks(files):
    split_files_ = []
    for file in files:
        split_files_.extend(file.split('!@#'))
    return split_files_

# for each passed split file, extract education and experience by splitting by double #
def extract_education_and_experience(split_files):
    education_experience = []
    for file in split_files:
        split_file = file.split('##')
        education_experience.append(split_file)
    return education_experience

def extract_jd_edu_and_exp(split_files):
    '''
    each of the split files has the format
    JD: <job description>
    ##
    Edu: <education>
    #!#
    Exp: <experience>
    #~#~
    Exp: <another_experience>
    #~#~
    ...
    
    Extract the job description, education and experience from each file, make the expereince a list of experiences
    '''
    # data/pm_3-8-years/
    jd_edu_exp = []
    for file in split_files:
        if len(file) < 10:
            continue
        split_file = file.split('##')
        print(split_file)
        input()
        job_description = split_file[0]
        edu_exp = split_file[1].split('#!#')
        education = edu_exp[0]
        experience = edu_exp[1].split('#~#~')
        # experience = [exp for exp in experience]
        jd_edu_exp.append([job_description, education, experience])
    return jd_edu_exp


def final_chunks(jd_edu_exp_element):
    jd = jd_edu_exp_element[0]
    education = jd_edu_exp_element[1]
    experience = jd_edu_exp_element[2]
    education_chunks = [education]
    experience_chunks = experience
    return jd, education_chunks, experience_chunks

def store_data(jd_edu_exp, filename='data.json'):
    data = {}
    for i, element in enumerate(jd_edu_exp):
        jd, education_chunks, experience_chunks = final_chunks(element)
        data[i] = {
            "jd": jd,
            "edu_chunks": education_chunks,
            "exp_chunks": experience_chunks
        }
    flname = input('Enter file name: ')
    if flname:
        filename = flname
    with open(f'data/{filename}', 'w') as f:
        json.dump(data, f, indent=4)

def chunking_pipeline(folder='data', filename='data.json'):
    files = open_files(folder)
    split_files = split_files_into_chunks(files)
    jd_edu_exp = extract_jd_edu_and_exp(split_files)
    store_data(jd_edu_exp, filename)

# def embed():
#     files = open_files()
#     split_files = split_files(files)
#     education_experience = extract_education_and_experience(split_files)
#     education_chunks, experience_chunks = final_chunks(education_experience[0])
#     education_embeddings = get_embedding(education_chunks)
#     experience_embeddings = get_embedding(experience_chunks)
#     return education_embeddings, experience_embeddings

if __name__ == '__main__':
    chunking_pipeline()