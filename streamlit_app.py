import streamlit as st

from client import COHERE
from util import parse_generated_text

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

        # st.write(f"""
        # ### Disclaimer
        #
        # """)
        #
        # st.write(f"""---""")

        st.subheader('Make a dish.')
        model_size = st.radio('Model size',
            ('small', 'medium', 'large'))
        query = st.text_input("What ingredients do you have?")

        if st.button('Find a recipe'):
            cohere = COHERE(api_key, model_size)

            with st.spinner(text='In progress'):
                ings, steps, name = process_prompt(cohere, query)
            st.subheader('Results.')
            st.write('# Name')
            st.write(ings)
            st.write('# Ings')
            st.write(ings)
            st.write('# Steps')
            st.write(steps)




    else:
        st.error("🔑 API Key Not Found!")
        st.info("💡 Copy paste your COHERE API key that you can find in User -> API Keys section once you log in to"
                " the COHERE API Playground")


if __name__ == '__main__':
    app()
