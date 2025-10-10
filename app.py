import streamlit as st
import os
import time
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv

# # Set up environment variables
# load_dotenv()
# os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")
# groq_api_key = os.getenv("GROQ_API_KEY")

# # Streamlit UI setup
# st.set_page_config(page_title="LawGPT")
# col1, col2, col3 = st.columns([1, 4, 1])
# st.title("Llama Model Legal ChatBot")
# st.markdown("""
#     <style>
#     div.stButton > button:first-child {
#         background-color: #ffd0d0;
#     }
#     div.stButton > button:active {
#         background-color: #ff6262;
#     }
#     div[data-testid="stStatusWidget"] div button {
#         display: none;
#     }
#     .reportview-container {
#         margin-top: -2em;
#     }
#     #MainMenu {visibility: hidden;}
#     .stDeployButton {display:none;}
#     footer {visibility: hidden;}
#     #stDecoration {display:none;}
#     button[title="View fullscreen"] {
#         visibility: hidden;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Reset conversation function
# def reset_conversation():
#     st.session_state.messages = []
#     st.session_state.memory.clear()

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "memory" not in st.session_state:
#     st.session_state.memory = ConversationBufferWindowMemory(k=2, memory_key="chat_history", return_messages=True)

# # Initialize embeddings and vector store
# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# db = FAISS.load_local("my_vector_store", embeddings, allow_dangerous_deserialization=True)
# db_retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# # Define the prompt template
# prompt_template = """
# <s>[INST]This is a chat template and As a legal chat bot , your primary objective is to provide accurate and concise information based on the user's questions. Do not generate your own questions and answers. You will adhere strictly to the instructions provided, offering relevant context from the knowledge base while avoiding unnecessary details. Your responses will be brief, to the point, and in compliance with the established format. If a question falls outside the given context, you will refrain from utilizing the chat history and instead rely on your own knowledge base to generate an appropriate response. You will prioritize the user's query and refrain from posing additional questions. The aim is to deliver professional, precise, and contextually relevant information pertaining to the Indian Penal Code.
# CONTEXT: {context}
# CHAT HISTORY: {chat_history}
# QUESTION: {question}
# ANSWER:
# </s>[INST]
# """
# prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question', 'chat_history'])

# # Initialize the LLM
# llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")

# # Set up the QA chain
# qa = ConversationalRetrievalChain.from_llm(
#     llm=llm,
#     memory=st.session_state.memory,
#     retriever=db_retriever,
#     combine_docs_chain_kwargs={'prompt': prompt}
# )

# # Display previous messages
# for message in st.session_state.messages:
#     with st.chat_message(message.get("role")):
#         st.write(message.get("content"))

# # Input prompt
# input_prompt = st.chat_input("Say something")

# if input_prompt:
#     with st.chat_message("user"):
#         st.write(input_prompt)

#     st.session_state.messages.append({"role": "user", "content": input_prompt})

#     with st.chat_message("assistant"):
#         with st.status("Thinking 💡...", expanded=True):
#             result = qa.invoke(input=input_prompt)
#             message_placeholder = st.empty()
#             full_response = "\n\n\n"

#             # Print the result dictionary to inspect its structure
#             #st.write(result)

#             for chunk in result["answer"]:
#                 full_response += chunk
#                 time.sleep(0.02)
#                 message_placeholder.markdown(full_response + " ▌")

#             # Print the answer
#             #st.write(result["answer"])

#         st.button('Reset All Chat 🗑️', on_click=reset_conversation)
#     st.session_state.messages.append({"role": "assistant", "content": result["answer"]})

#new look 
# Set up environment variables
load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Streamlit UI setup with modern theme
st.set_page_config(
    page_title="LegalBot AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern CSS styling
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Title styling */
    h1 {
        color: white !important;
        font-weight: 700 !important;
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Chat container */
    .stChatMessage {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* User message */
    [data-testid="stChatMessageContent"] {
        background: transparent;
    }
    
    /* Chat input */
    .stChatInputContainer {
        background: white;
        border-radius: 25px;
        padding: 0.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102,126,234,0.3);
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102,126,234,0.4);
    }
    
    div.stButton > button:active {
        transform: translateY(0);
    }
    
    /* Status widget */
    .stStatus {
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        padding: 1rem;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}
    button[title="View fullscreen"] {visibility: hidden;}
    div[data-testid="stStatusWidget"] div button {display: none;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255,255,255,0.5);
    }
    
    /* Card effect for chat area */
    [data-testid="stVerticalBlock"] > div {
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(10px);
    }
    </style>
""", unsafe_allow_html=True)

# Header with icon
st.markdown('<h1>⚖️ LegalBot AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your AI-Powered Legal Assistant for Indian Penal Code</p>', unsafe_allow_html=True)

# Reset conversation function
def reset_conversation():
    st.session_state.messages = []
    st.session_state.memory.clear()
    st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(k=2, memory_key="chat_history", return_messages=True)

# Initialize embeddings and vector store
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
db = FAISS.load_local("my_vector_store", embeddings, allow_dangerous_deserialization=True)
db_retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# Define the prompt template
prompt_template = """
<s>[INST]This is a chat template and As a legal chat bot, your primary objective is to provide accurate and concise information based on the user's questions. Do not generate your own questions and answers. You will adhere strictly to the instructions provided, offering relevant context from the knowledge base while avoiding unnecessary details. Your responses will be brief, to the point, and in compliance with the established format. If a question falls outside the given context, you will refrain from utilizing the chat history and instead rely on your own knowledge base to generate an appropriate response. You will prioritize the user's query and refrain from posing additional questions. The aim is to deliver professional, precise, and contextually relevant information pertaining to the Indian Penal Code.
CONTEXT: {context}
CHAT HISTORY: {chat_history}
QUESTION: {question}
ANSWER:
</s>[INST]
"""
prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question', 'chat_history'])

# Initialize the LLM
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")

# Set up the QA chain
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    memory=st.session_state.memory,
    retriever=db_retriever,
    combine_docs_chain_kwargs={'prompt': prompt}
)

# Create columns for better layout
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # Welcome message for first-time users
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0;'>
            <h3 style='color: #667eea; margin-bottom: 1rem;'>👋 Welcome to LegalBot AI</h3>
            <p style='color: #555; font-size: 1.1rem;'>Ask me anything about the Indian Penal Code and I'll provide accurate, concise legal information.</p>
            <p style='color: #888; margin-top: 1rem; font-size: 0.9rem;'>Powered by Llama 3 70B and Google AI</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message.get("role"), avatar="👤" if message.get("role") == "user" else "⚖️"):
            st.write(message.get("content"))

# Input prompt
input_prompt = st.chat_input("Ask a legal question...", key="chat_input")

if input_prompt:
    with col2:
        with st.chat_message("user", avatar="👤"):
            st.write(input_prompt)
        
        st.session_state.messages.append({"role": "user", "content": input_prompt})
        
        with st.chat_message("assistant", avatar="⚖️"):
            with st.status("🤔 Analyzing your question...", expanded=True):
                result = qa.invoke(input=input_prompt)
                message_placeholder = st.empty()
                full_response = ""
                
                # Streaming response
                for chunk in result["answer"]:
                    full_response += chunk
                    time.sleep(0.02)
                    message_placeholder.markdown(full_response + " ▌")
                
                message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": result["answer"]})

# Reset button in sidebar
with col3:
    if st.button('🗑️ Clear Chat', use_container_width=True):
        reset_conversation()