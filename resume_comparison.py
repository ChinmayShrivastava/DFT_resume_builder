import os
import json
from search import *
from prompts import COMPARE_RESUME
# from dotenv import load_dotenv
# load_dotenv()

# openai.api_key = os.environ.get('OPENAI_API_KEY')

# def gpt3_3turbo_completion(messages, summarymodel='gpt-4'): # 'gpt-3.5-turbo' or 'gtp-4'

# 	temperature = 0.2
# 	max_length = 500
# 	top_p = 1.0
# 	frequency_penalty = 0.0
# 	presence_penalty = 0.1

# 	# making API request and error checking
# 	print("making API request")
# 	try:
# 		response = openai.ChatCompletion.create(
# 			model=summarymodel, 
# 			messages=messages, 
# 			temperature=temperature, 
# 			max_tokens=max_length, 
# 			top_p=top_p, 
# 			frequency_penalty=frequency_penalty, 
# 			presence_penalty=presence_penalty)
# 	except openai.error.RateLimitError as e:
# 		print("OpenAI API rate limit error! See below:")
# 		print(e)
# 		return None, None, None
# 	except Exception as e:
# 		print("Unknown OpenAI API error! See below:")
# 		print(e)
# 		return None, None, None
	
# 	return response['choices'][0]['message']['content']

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

# open embeddings.json
def open_embeddings_json():
    for filename in os.listdir('data'):
        if filename.endswith('.json'):
            print(filename)
    filename = input('Enter filename: ')
    if filename:
        with open(f'data/{filename}', 'r') as f:
            embeddings = json.load(f)
    else:
        print("No filename entered. Using default embeddings.json")
        filename = 'embeddings.json'
        with open('data/embeddings.json', 'r') as f:
            embeddings = json.load(f)
    # with open('data/embeddings.json', 'r') as f:
    #     embeddings = json.load(f)
    return embeddings

if __name__ == '__main__':
    # Load data
    data = open_data_json()[0]
    # Load embeddings
    embeddings = open_embeddings_json()
    JOB_DESCRIPTION = '''The JD:
We are seeking an innovative Product and Growth Lead to drive our product development and user expansion strategies. As our 1st PM, you’ll be working to enhance our product offerings and extend our market reach to establish a dominant position in the industry.
Job Responsibilities:
Direct the full product development cycle, from initial testing to project management, ensuring a seamless user experience.
Craft and execute growth strategies to boost product uptake and engagement.
Partner with the design team to continuously improve and innovate the product's design, focusing on user-centric experiences.
Work on growth initiatives through collaboration with marketing, creative, and community teams.
Requirements:
2+ years in product management, with a strong preference for experience in consumer or video products.
Experience in successful marketing and growth initiatives.
Robust creative and analytical abilities, with a strategic approach to product evolution and user base growth.
Effective communication skills and a collaborative spirit to work synergistically with various teams.
A dynamic, startup mindset with a zeal for innovation and a passion for working in a fast-paced environment.
A plus if complemented by an artistic interest and background.
This position is in-person.'''
    NOTES = '''I have a strong interest in filmmaking and possess over three years of experience in account acquisition, product lifecycle management, and growth strategies that I cultivated during my time at Palantir. I am looking forward to applying my technical expertise and strategic insights to contribute to Pika's pioneering product leadership, foster its growth, and boost its adoption.

In my previous role, I successfully led the development of custom enterprise products, generating revenue of $24 million across various accounts. This success was achieved through identifying market opportunities, creating user-focused solutions, and building robust relationships at all levels within the organization, from end-users to executive suite. More recently, I was at the helm of a 12-person engineering team where I drove the acquisition and upscaling of manufacturing accounts by developing custom AI solutions.

Since July, I have been conducting a series of hackathons and bootcamps for technical users. These efforts have resulted in nine new contracts and increased active engagement with existing clients. My role at Palantir and for our clients encompassed everything from product roadmap planning and execution to designing architecture, scoping use cases, and fostering user community growth.

I am particularly proud of leading the design and implementation efforts for Palantir's Scenarios product as the primary user-facing associate. This product was adopted by our entire user base within six months of launch thanks to simplified UX, scalable workflows, and successful client showcases.

I believe in the power of collaboration and always seek to work with teams composed of individuals who are exceptional, kind-hearted, and motivated by collective achievement. I'm committed to providing the resources my team needs, fostering a sense of shared responsibility, and ensuring skills are allocated in a way that meets the business needs effectively.

My passion for filmmaking and technology combined with analytical expertise, aligns well with Pika's mission to revolutionize expression through AI. I am excited about the opportunity to contribute to its rapid growth. I am eager to discuss how I can apply my experience and growth-oriented product expertise to help position Pika as a leader in AI-powered video creation, democratize creative tools, and establish a new standard.'''
    results = vector_search(JOB_DESCRIPTION, embeddings, data)[0:3]
    # fs = []
    fs_example = """Explain step-by-step how to write the resume and then output the resume as illustrated in some examples before.
    """
    i = 0
    for result in results:
        fs_example += f"{i+1}. {result} \n"
    fs_example += f"""Job Description: {JOB_DESCRIPTION}
Notes: {NOTES}"""
    with open('data/final_prompt.txt', 'w') as f:
        f.write(fs_example)