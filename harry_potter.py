import streamlit as st
import requests

from openai import OpenAI

st.title("Harry Potter Fan App")


# Dropdown to select a character
#character_name = st.selectbox("Choose a character", ["Harry Potter", "Hermione Granger", "Ron Weasley"]) # Add more names as needed

client = OpenAI()


def get_character_data(name):
    url = f"https://hp-api.onrender.com/api/characters"
    response = requests.get(url)
    if response.status_code == 200:
        characters = response.json()
        for c in characters:
                if c["name"].lower() == name:
                    return c
    return None



def generate_poem(name):
    try:
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": "You are an expert poet. You write poems. Your poems are short, generally less than 150 words."
            },
            {
            "role": "user",
            "content": f"Write a Harry Potter charater poem starring {name} highlighting his abilities"
            },
        ],
        temperature=1,
        max_tokens=490,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


# Text input to select a character
character_name = st.text_input("Choose a character")

# Button to fetch character data
st.button("Reveal Character Secrets!")
    # Fetch and display data here in the next step
    #pass

# Display the input result
if character_name:
    st.write(f"Your character is : {character_name}")
    response = get_character_data(character_name.lower())
    if response:
        st.markdown(response["name"])
        st.image(response['image'], width=200) # Display image
        st.write(f"*Name:* {response['name']}")
        st.write(f"*House:* {response['house']}")
        st.write(f"*Species:* {response['species']}")
        st.write(f"*Patronus:* {response['patronus']}")
        gpt_response = generate_poem(character_name)
        st.write(f"*Poem:* {gpt_response}")
        

# character_data = get_character_data(character_name.lower())

