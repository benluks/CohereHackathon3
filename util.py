import ast
import pandas as pd
from typing import List


def format_list(ls: List[str]):
    """
    Utility function to convert list into model-digestible format 
    """
    return "; ".join(ls)


def load_recipes(path='tst_recipes.csv'):
    """
    Load recipes from file path
    """
    df = pd.read_csv(path)
    # read stringified lists as lists
    df.ingredients = df.ingredients.map(ast.literal_eval)
    df.steps = df.steps.map(ast.literal_eval)

    return df[["ingredients", "steps", "name"]]