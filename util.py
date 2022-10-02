import ast
import pandas as pd
from typing import List


def format_list(ls: List[str]):
    """
    Utility function to convert list into model-digestible format 
    """
    return "; ".join(ls)


def parse_formatted_list(formatted_list: str):
    return formatted_list.split()

def load_recipes(path='tst_recipes.csv'):
    """
    Load recipes from file path
    """
    df = pd.read_csv(path)
    # read stringified lists as lists
    df.ingredients = df.ingredients.map(ast.literal_eval)
    df.steps = df.steps.map(ast.literal_eval)

    return df[["ingredients", "steps", "name"]]


def parse_generated_text(gen_text):
    
    lines = gen_text.split('\n')
    additional_ings = lines[0].split('; ')
    steps = lines[1].replace("Directions:", "").split("; ")
    name = lines[2].replace("Name:", "")
    
    return additional_ings, steps, name

def remove_one_recipe_from_prompt(prompt):
    """
    Remove last recipe from prompt to shorten length
    """
    recipes = prompt.split("--")
    del recipes[-2]
    return "--".join(recipes)

