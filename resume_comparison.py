import os
import json
from search import *
from prompts import COMPARE_RESUME
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import openai
import os
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
    JOB_DESCRIPTION = '''JD:
About the Position
We are looking for Quantitative Traders to help us find and trade on price inefficiencies, develop models, manage risk, investigate new products, and push into new business areas. Our trading is based on our own proprietary models, and on busy days we engage in over a million trades across 200 trading venues around the world.

Our trading desks are central to our collaborative and cooperative office environment. You can expect to work side by side with experienced Traders who are committed to teaching, guiding, and supporting our newest hires from day one. Through hands-on, interactive training, you’ll acquire significant, real trading responsibilities within weeks to months of being on the desk. In parallel, you will participate in our robust year-long firmwide educational curriculum.

A profitable trading strategy is only as strong as the technology it runs on, and we consider ourselves as much a technology company as a trading firm. While exposure to a particular programming language is not required, general programming experience is a plus.

If you’d like to learn more, you can read about our interview process and meet some of our newest hires.

About You
We don’t expect you to have a background in finance or any other specific field—we’re looking for smart people who enjoy solving interesting problems. We’re more interested in how you think and learn than what you currently know. You should be:

A critical thinker with a strong quantitative mind
A collaborative problem-solver who enjoys working on a team
Able to make decisions quickly in a fast-paced environment
Proactive, reliable, and courteous with strong organizational and communication skills
Eager to ask questions, admit mistakes, and learn new things
Fluent in English'''
    NOTES = '''I have a Master of Engineering in Innovation Management and Entrepreneurship from Brown University, with an upper second class degree in Mathematics with Statistics from King's College London. During my undergraduate studies, I took courses in a variety of statistics and mathematical finance courses, including Applied Differential Equations, Mathematical Finance, Probability Theory, Statistical Modelling, Statistical Inference, and Time Series Analysis. My degree coursework also involved generating a multivariable linear regression model in R to analyze the impact of various factors on housing prices in different areas.

In my professional experience, I worked with Xcede as a Senior Consultant from November 2021 to February 2023. This role had me proactively organize and lead international client meetings to establish lasting relationships and maintain a steady stream of new business. I performed quantitative analysis on market data and communicated these insights to our internal team and our clients.

I was in charge of managing key accounts and facilitated communication between senior stakeholders to ensure a clear, streamlined process and strategy goals. I led a cross-functional team to efficiently scale and meet deadlines. In addition, I conducted weekly training sessions for incoming graduate hires. Through these efforts, I generated over 190,000 dollars in direct revenue in fiscal year 2022, consistently outperforming non-financial key performance indicators.

Before that, I was a Technology Risk Consultant at Ernst & Young from August 2021 to October 2021. I conducted walkthroughs with clients to review information technology processes and assure the data accuracy of financial audits. I also managed client relationships by communicating clearly about their goals and timelines. Moreover, I was responsible for creating detailed documentations of IT processes and controls, ensuring that evidence was sufficient and up to standard.'''
    results = vector_search(JOB_DESCRIPTION, embeddings, data)[0:3]
    fs = []
    fs_example = """Explain step-by-step how to write the resume and then output the resume as illustrated in some examples before.
    """
    i = 0
    for result in results:
        fs_example += f"{i+1}. {result} \n"
    fs_example += f"""Job Description: {JOB_DESCRIPTION}
Notes: {NOTES}"""
    with open('data/final_prompt.txt', 'w') as f:
        f.write(fs_example)