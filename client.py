import cohere
from dotenv import load_dotenv
import numpy as np
import os

from load_recipes import load_recipes

# load api_key
load_dotenv()

# GLOBALS
API_KEY = os.getenv('API-KEY')
MODEL = 'small'
RECIPES_FILE = './test_recipes.csv'
MAX_PROMPT_LEN = 2048
NUM_GEN_CHARS = 200

# init client
co = cohere.Client(API_KEY)

recipes = load_recipes(RECIPES_FILE)
ingredients = ["; ".join(ings) for ings in recipes.ingredients]

embeddings = np.array(co.embed(model=MODEL,texts=ingredients).embeddings)


# response.embeddings is a n-length list of 1024 elements each

print(len(response.embeddings[1]))

