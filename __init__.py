# Import necessary libraries
import databutton as db
import streamlit as st

# Import Langchain modules
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents.tools import Tool
from langchain import OpenAI
from langchain.agents import initialize_agent
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# Streamlit UI Callback
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chains import LLMMathChain
from langchain.memory import ConversationBufferMemory

import openai


# Import modules related to streaming response
import os
import time

st.title("Try AELM By Mundus")
st.markdown(
    """ 
    The AELM (Auto Execution Language Model) is the backbone of Mundus, Have traditional LLM capabilities, but with special training and architectural adjustments to reduce costs and specifically train to perform agent tasks.
    """
)

st.write(
    """
    👋 Welcome To Mundus's AELM Playground.
    Your every-day assisant to connect the 'Mundus'...
"""
)

# Get the user's question input
question = st.chat_input("Let's change the world.")

# Get the API key from the secrets manager
API_KEY = os.environ["API_KEY"]

# Initialize chat history if it doesn't already exist
if "messages" not in st.session_state:
    st.session_state.messages = []

from Mundus.llm.base import load_llm()
from Mundus.tools.base import available_tools
from available_tools import import_all_tools()
llm = load_llm()
import_all_tools()

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history")


# Set up the tool for responding to general questions
tools = [
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math.",
    )
]

# Set up the tool for performing internet searches
search_tool = Tool(
    name="DuckDuckGo Search",
    func=search.run,
    description="Useful for when you need to do a search on the internet to find information that another tool can't find. Be specific with your input or ask about something that is new and latest.",
)
tools.append(search_tool)

# Initialize the Zero-shot agent with the tools and language model
conversational_agent = initialize_agent(
    agent="conversational-react-description",
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=10,
    memory = st.session_state.memory
)

# Display previous chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process the user's question and generate a response
if question:
    # Display the user's question in the chat message container
    with st.chat_message("user"):
        st.markdown(question)

    # Add the user's question to the chat history
    st.session_state.messages.append({"role": "user", "content": question})

    # Generate the assistant's response
    with st.chat_message("assistant"):
        # Set up the Streamlit callback handler
        st_callback = StreamlitCallbackHandler(st.container())
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = conversational_agent.run(question, callbacks=[st_callback])

        # Simulate a streaming response with a slight delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)

            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")

        # Display the full response
        message_placeholder.info(full_response)

    # Add the assistant's response to the chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
# Written at