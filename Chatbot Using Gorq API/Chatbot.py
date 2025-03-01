import os
import streamlit as st
import requests
import tiktoken
import openai

# Set the base URL and the API key for Groq (through OpenAI compatibility)
GROQ_API_KEY = "YOUR API KEY"
openai.api_key = GROQ_API_KEY
openai.api_base = "https://api.groq.com/openai/v1"  # Correct base URL for Groq

# Initialize tiktoken tokenizer
tokenizer = tiktoken.get_encoding("cl100k_base")  # Use the correct encoding for the model

# Function to count tokens
def count_tokens(text):
    return len(tokenizer.encode(text))

# Function to send a message to the Groq API and get the response
def chat_with_groq(messages):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",  # Replace with the correct model name
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(openai.api_base + "/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code}")
        st.error(response.text)
        return None

# Streamlit app
def main():
    st.title("🤖 Chatbot")
    st.write("Welcome to the Groq Chatbot! Type your message below and press Enter.")

    # Initialize session state to store conversation history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    # Display previous messages
    for message in st.session_state.messages:
        if message["role"] != "system":  # Don't display system messages
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # Get user input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message to the conversation history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Display user message
        with st.chat_message("user"):
            st.write(user_input)

        # Count tokens for the user input
        user_tokens = count_tokens(user_input)
        st.write(f"User input tokens: {user_tokens}")

        # Get bot response from Groq API with loading spinner
        with st.spinner("Getting response from Groq..."):
            bot_response = chat_with_groq(st.session_state.messages)

        if bot_response:
            # Extract the bot's response
            bot_message = bot_response["choices"][0]["message"]["content"]

            # Add bot response to the conversation history
            st.session_state.messages.append({"role": "assistant", "content": bot_message})

            # Display bot response
            with st.chat_message("assistant"):
                st.write(bot_message)

            # Count tokens for the bot's response
            bot_tokens = count_tokens(bot_message)
            st.write(f"Bot response tokens: {bot_tokens}")

            # Display total tokens used in the API call
            total_tokens = bot_response["usage"]["total_tokens"]
            st.write(f"Total tokens used: {total_tokens}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
