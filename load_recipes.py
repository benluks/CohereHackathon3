import pandas as pd
import ast


def load_recipes(path='tst_recipes.csv'):
    """
    Load recipes from file path
    """
    df = pd.read_csv(path)
    # read stringified lists as lists
    df.ingredients = df.ingredients.map(ast.literal_eval)
    df.steps = df.steps.map(ast.literal_eval)

    return df[["ingredients", "steps", "name"]]