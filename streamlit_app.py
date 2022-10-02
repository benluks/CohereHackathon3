import streamlit as st

from client import CohereClient
from util import parse_formatted_list, parse_generated_text

# Using the streamlit cache
def process_prompt(cohere, query):

    recipes = cohere.generate_from_query(query)[0].text
    ings, steps, name = parse_generated_text(recipes)
    return ings, steps, name


def app():
    api_key = st.sidebar.text_input("COHERE API Key:", type="password", value='XXX')

    if api_key:

        # Setting up the Title
        st.title("Recipe generator powered by COHERE")

        st.write("Get a recipe for a dish based on the ingredients you provide,"
                 " the type of cuisine you prefer and the kitchen utensils you have at your disposal.")

        st.image("world_map.jpg", use_column_width=True)


        st.write("---")

        st.subheader('Make a dish.')
        model_size = st.radio('Model size',
            ('small', 'medium', 'large'), index=2)
        query = st.text_input("What ingredients do you have?")

        if st.button('Find a recipe'):
            cohere = CohereClient(api_key, model_size)

            # with st.spinner(text='In progress'):
            #     ings, steps, name = process_prompt(cohere, query)
            name = "baked beans"
            input_ings = parse_formatted_list(query)
            ings = [' brown sugar', 'salt', 'black pepper']
            steps = ['cook ground chuck with onions until meat crumbles & is browned', 'add remaining ingredients and mix', 'pour into a greased 9x9 inch baking dish and top with a little brown sugar', 'bake at 375 degrees for 1 1/2 to 2 hours']
            st.subheader(name.title())
            # st.write(f'## {name}')
            st.write('### Ingredients')
            for input_ing in input_ings:
                st.write(f"* {input_ing.strip().capitalize()}")
            st.write("Suggested Additions")
            for ing in ings:
                st.write(f"* {ing.strip().capitalize()}")
            st.write('### Directions')
            for i, step in enumerate(steps):
                st.write(f"{i+1}. {step.strip().capitalize()}")




    else:
        st.error("🔑 API Key Not Found!")
        st.info("💡 Copy paste your COHERE API key that you can find in User -> API Keys section once you log in to"
                " the COHERE API Playground")


if __name__ == '__main__':
    app()
