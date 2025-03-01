# Groq Chatbot with Streamlit

This is a simple Streamlit application that allows users to chat with a chatbot powered by the Groq API, using OpenAI-compatible endpoints and a `llama-3.3-70b-versatile` model. It uses the Groq API for generating responses and integrates token counting with the `tiktoken` library.

## Features

- Chat interface built using Streamlit.
- Seamless communication with the Groq API.
- Token counting for both user inputs and bot responses.
- Real-time responses with a loading spinner while waiting for the API to respond.

## Prerequisites

Before running this app, make sure you have the following dependencies installed:

1. **Python 3.7+**
2. **Required Python libraries**: 
    - `streamlit`
    - `requests`
    - `tiktoken`
    - `openai`

You can install the required libraries using `pip`:

pip install streamlit requests tiktoken openai


## Setup Instructions

1. Clone the Repository:
    [https://github.com/Varun2573/Python-projects/tree/main/Chatbot Using Gorq API](https://github.com/Varun2573/Python-projects/tree/main/Chatbot%20Using%20Gorq%20API)

2. Set your Groq API key: 
    In the code, replace the GROQ_API_KEY variable with your own Groq API key.

3. Run the Streamlit Application: 
    Navigate to the project directory and run the Streamlit app:

         streamlit run Chatbot.py

        This will open the app in your default web browser.

## Application Flow

1. The app initializes the chatbot with a system message that states the bot is a helpful assistant.
2. Users can type messages in the input field and submit them.
3. The user message is sent to the Groq API, which generates a response.
4. The bot’s response, as well as the number of tokens used in the interaction, is displayed on the interface.

## Token Counting

This application includes a token counter for both user inputs and bot responses. The token counts are based on the tiktoken library and are displayed during the conversation.

    1. User input tokens: The number of tokens used by the user's message.
    2. Bot response tokens: The number of tokens used in the bot's reply.
    3. Total tokens used: The combined total of tokens used by both the user input and the bot's response for a given API call.

## Example Conversation

User: "Hello, how are you?"

Bot: "I'm good, thank you for asking! How can I assist you today?"

## Notes

1. The app interacts with the Groq API using OpenAI-compatible endpoints.
2. Ensure that your Groq API key is correctly configured in the code.
