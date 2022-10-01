from annoy import AnnoyIndex
import cohere
from dotenv import load_dotenv
import numpy as np
import os
import re

from templates import prompt
from util import format_list, load_recipes

# load api_key
load_dotenv()

# GLOBALS
API_KEY = os.getenv('API-KEY')
MODEL = 'small'
TRUNCATE = "LEFT"
RECIPES_FILE = './test_recipes.csv'
MAX_PROMPT_LEN = 2048
NUM_GEN_CHARS = 200
NUM_NEIGHBOURS = None # default to entire dataset

# init client
co = cohere.Client(API_KEY)
recipes = load_recipes(RECIPES_FILE)
ingredients = [format_list(ings) for ings in recipes.ingredients]

# compute embeddings
embeddings = np.array(co.embed(model=MODEL,texts=ingredients, truncate=TRUNCATE).embeddings)


"""
Search index for nearest neighbor semantic search
"""
# Create the search index, pass the size of embedding
search_index = AnnoyIndex(embeddings.shape[1], 'angular')
# Add all the vectors to the search index
for i in range(embeddings.shape[0]):
    search_index.add_item(i, embeddings[i])

search_index.build(10) # 10 trees


"""
Query Embedding (from user input)
"""
query = "eggs; tomatoes; chicken; lemon; ginger; black pepper"
query_embedding = co.embed(texts=[query], model=MODEL, truncate=TRUNCATE).embeddings[0]
similars, dists = search_index.get_nns_by_vector(
  query_embedding, 
  n=NUM_NEIGHBOURS if NUM_NEIGHBOURS else len(embeddings), 
  include_distances=True
  )


"""
Generating
"""
gen_query = "This program makes a recipe from a list of ingredients\n\n"
similar_recipes = recipes.iloc[similars[:10]]
for i, (ings, steps, name) in similar_recipes.iterrows():
  gen_query += prompt.format(format_list(ings), format_list(steps), re.sub(' +', ' ', name.strip()))

print(gen_query)
