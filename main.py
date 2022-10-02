from client import generate_from_query
from util import parse_generated_text

if __name__ == '__main__':
    query = input("What ingredients do you have? ")

    recipes = generate_from_query(query)[0].text
    
    ings, steps, name = parse_generated_text(recipes)
    print(name)
    print(ings)
    print(steps)