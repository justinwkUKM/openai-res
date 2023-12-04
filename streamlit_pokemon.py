import streamlit as st
import requests
# This code is for v1 of the openai package: pypi.org/project/openai
from openai import OpenAI


client = OpenAI()

def get_pokemon_info(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
# Function to parse abilities from JSON
def parse_abilities(data):
    abilities = []
    for item in data['abilities']:
        ability_name = item['ability']['name']
        abilities.append(ability_name)
    return abilities

st.title('Pokémon Fan App!')

st.write("Enter the name of your favorite Pokémon:")

# Text input for favorite Pokémon
favorite_pokemon = st.text_input("Favorite Pokémon")

# Display the input result
if favorite_pokemon:
    st.write(f"Your favorite Pokémon is: {favorite_pokemon}")
    response = get_pokemon_info(favorite_pokemon.lower())
    if response:
        
        # st.write(response["sprites"]["front_default"])
        st.image(response["sprites"]["front_default"], caption=favorite_pokemon)
        abilities = parse_abilities(response)
        # st.json(response, expanded=True)
        st.write("List of Abilities:")
        # Display abilities
        for ability in abilities:
            st.write("- ", ability)
        response_openai = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": "You are an expert story writer. You write stories. Your stories are short, generally less than 150 words."
            },
            {
            "role": "user",
            "content": f"Write a Pokeman story starring {favorite_pokemon} highlighting his abilities; {abilities}"
            },
        ],
        temperature=1,
        max_tokens=490,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        st.write(response_openai.choices[0].message.content)

 
    