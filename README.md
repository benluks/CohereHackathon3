# CohereHackathon3

Recipe generator using [cohere](https://cohere.ai/) and [annoy](https://github.com/spotify/annoy), built for the [Cohere AI Hackathon #3](https://lablab.ai/event/cohere-ai-hackathon-classify).

## Quickstart

Install dependencies:
`pip install -r requirements.txt`

You'll need to make a `.env` file. Place it in the root directory. It should contain your api key as follows:

`API-KEY=<your-api-key>`

To run the application:

`python main.py`

You'll be prompted with

`What ingredients do you have?`

Enter the ingredients in lower case separated by semicolon-space, eg: `tomatoes; onions; etc.;`. The output will be 3 lines:

1. The name of the generated recipe
2. The additional ingredients (formatted as a list)
3. The directions (formatted as a list)


## Data

An example file for the data can be found in `./test_recipes.csv`. It is a csv file with 1000 recipes.
The `util.py` module contains a function `load_recipes()` that accepts a filepath and returns a `pandas.DataFrame` containing the columns
* `ingredients: List[str]`
* `steps: List[str]`
* `name: str` 


## TODO

- [ ] Come up with a catchy name
- [ ] Suggest ingredients boolean: Whether to add ingredients or not
