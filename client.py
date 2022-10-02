from annoy import AnnoyIndex
import cohere
from dotenv import load_dotenv
import numpy as np
import re

from templates import prompt_header, prompt_item
from util import format_list, load_recipes, remove_one_recipe_from_prompt

# load api_key
load_dotenv()

# GLOBALS
TRUNCATE = "LEFT"
RECIPES_FILE = './test_recipes.csv'
# MAX_PROMPT_LEN = 2048
# NUM_GEN_CHARS = 200
NUM_NEIGHBOURS = None # default to entire dataset

class COHERE:
	def __init__(self, api_key, model_size):
		self.model_size = model_size
		self.co = cohere.Client(api_key)
		self.recipes = load_recipes(RECIPES_FILE)
		self.ingredients = [format_list(ings) for ings in self.recipes.ingredients]

		# compute embeddings
		self.embeddings = np.array(self.co.embed(model=model_size,texts=self.ingredients, truncate=TRUNCATE).embeddings)


		"""
		Search index for nearest neighbor semantic search
		"""
		# Create the search index, pass the size of embedding
		self.search_index = AnnoyIndex(self.embeddings.shape[1], 'angular')
		# Add all the vectors to the search index
		for i in range(self.embeddings.shape[0]):
			self.search_index.add_item(i, self.embeddings[i])

		self.search_index.build(10) # 10 trees


	"""
	Query Embedding (from user input)
	"""

	def get_nns_from_query(self, query):
		"""
		take query as input, embed, and return similar indices from recipes
		"""
		query_embedding = self.co.embed(texts=[query], model=self.model_size, truncate=TRUNCATE).embeddings[0]

		similars_ids, _ = self.search_index.get_nns_by_vector(
			query_embedding,
			n=NUM_NEIGHBOURS if NUM_NEIGHBOURS else len(self.embeddings),
			include_distances=True
		)

		return similars_ids



	"""
	Generating
	"""
	def build_prompt_from_similars(self, similar_ids, query, n=10):

		prompt = prompt_header
		similar_recipes = self.recipes.iloc[similar_ids[:n]]

		for _, (ings, steps, name) in similar_recipes.iterrows():
			prompt += prompt_item.format(format_list(ings), format_list(steps), re.sub(' +', ' ', name))

		prompt += f"Ingredients:{query}"

		return prompt


	def generate_recipe(self, prompt):
		"""
		Generate recipe from cohere API. If query is too long,
		delete last recipe
		"""
		while True:
			try:
				response = self.co.generate(
					model=self.model_size,
					prompt=prompt,
					max_tokens=200,
					temperature=1,
					k=3,
					p=0.75,
					frequency_penalty=0,
					presence_penalty=0,
					stop_sequences=['--'],
					return_likelihoods='NONE'
				)
				return response.generations

			except cohere.error.CohereError:
				prompt = remove_one_recipe_from_prompt(prompt)


	def generate_from_query(self, query):
		"""
		Function to implement logic of this module end-to-end
		"""
		print(query)
		similar_ids = self.get_nns_from_query(query)
		prompt = self.build_prompt_from_similars(similar_ids, query)
		generations = self.generate_recipe(prompt)

		return generations
