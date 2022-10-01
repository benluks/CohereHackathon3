# CohereHackathon3

## Quickstart

`pip install -r requirements.txt`

You'll need a `.env`. Place it in the root directory. It should contain your api key as follows:

`API-KEY=<your-api-key>`

## Data

An example file for the data can be found in `./test_recipes.csv`. It is a csv file with 1000 recipes.
The `load_recipes.py` module contains a function `load_recipes()` that accepts a filepath and returns a dataframe containing the columns
* `ingredients: List[str]`
* `steps: List[str]`
* `name: str` 


## TODO

- [ ] Come up with a catchy name
- [ ] Suggest ingredients boolean: Whether to add ingredients or not
