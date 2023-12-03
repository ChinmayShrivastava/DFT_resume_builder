from chunker import *
from agents import *
from dfs import *
from embed import *
from prompts import *
from search import *
from resumebreaker import *

def template_upload_pipeline():
    chunking_pipeline()
    informalize_pipeline()
    embed_pipeline()
    cot_pipeline()

if __name__ == '__main__':
    template_upload_pipeline()