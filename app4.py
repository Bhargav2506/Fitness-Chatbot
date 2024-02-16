import os
import requests
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import openai

# Replace with your API key
OPENAI_API_KEY = "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"

def get_calories(food_item):
    api_url = f'https://api.api-ninjas.com/v1/nutrition?query={food_item}'
    response = requests.get(api_url, headers={'X-Api-Key': 'TIqhW4mjtYg0uHi2Pm9nDQ==bZMSMgQ6otBaFUao'})
    if response.status_code == requests.codes.ok:
        calorie_info = response.json()[0]["calories"]  # assuming the response is a list of food items, and you want the first one
        return f"The calorie content of {food_item} is {calorie_info} calories."
    else:
        return f"I couldn't find information about the calorie content of {food_item}. Please provide more specific details or check the API's documentation."

def handle_user_input(user_input):
    # Use a supported model for generating responses
    model_name = "EleutherAI/gpt-neo-1.3B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Tokenize the user input
    inputs = tokenizer(user_input, return_tensors="pt").input_ids

    # Generate a response from the model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You: " + user_input}
        ],
        api_key=OPENAI_API_KEY
    )

    # Extract the generated text from the response object
    try:
        generated_text = response['choices'][0]['message']['content']
    except Exception as e:
        generated_text = str(response)

    return generated_text

# Set up app
st.set_page_config(
    page_title="Fitness Chatbot 🦾",
    page_icon="🦾",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
    body {
        background-color: #ff8b27;
    }
    .stTextInput {
        background-color: #ff8b27;
        border: 1px solid #cccccc;
        padding: 10px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)
st.title('Fitness Chatbot 🦾')
st.write('Hello I am a fitness bot ask me question about fitness and nutrition related queries....!')

# Main loop for interacting with the chatbot
user_input = st.text_input("You: ", key="user_input")
if user_input:
    response = handle_user_input(user_input)
    st.markdown(f"<div style='background-color: #0074D9; padding: 10px; color: white;'>Bot: {response}</div>", unsafe_allow_html=True)

# Box for getting the food name and displaying calories
st.sidebar.title('Calories Checker')
food_name = st.sidebar.text_input('Enter Food Name:', key="food_name")
if food_name:
    calorie_info = get_calories(food_name)
    st.sidebar.markdown(f"<div style='background-color: #0074D9; padding: 10px; color: white;'>{calorie_info}</div>", unsafe_allow_html=True)
