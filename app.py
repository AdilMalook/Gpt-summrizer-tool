# ------ Import Libraries
import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from streamlit_chat import message
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory,ConversationSummaryMemory,ConversationBufferWindowMemory)

api_key_streamlit_secrets = st.secrets["openai"]["api_key"]

# ------ Session variable 
if 'conversation' not in st.session_state:
    st.session_state['conversation']= None
if 'messages' not in st.session_state:
    st.session_state['messages']= []
if 'API_Key' not in st.session_state:
    st.session_state['API_Key'] =''
if 'trial_count' not in st.session_state:
    st.session_state['trial_count'] = 0
if 'is_demo_key' not in st.session_state:
    st.session_state['is_demo_key'] = False

# ----- BackEnd M<odel Implimentation 
def UserInput_Click(Userinput,api_key):

    if st.session_state['conversation'] is None:

        llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            api_key=api_key,
            max_tokens=500
        )
    
        st.session_state['conversation'] =  ConversationChain(
        llm=llm,
        verbose=True,
        memory=ConversationBufferMemory()
    )
    
    response = st.session_state['conversation'].predict(input=Userinput)

    return response

# ----- Home Page Setting 
st.set_page_config(page_title="GPT With Summarizer Tool", page_icon=":earth_americas:",layout="centered")

# ------ Side Bar Design And Code
st.sidebar.title("GPT With Summarizer Tool")
user_api_key=st.sidebar.text_input("Enter OpenAI Api Key",type="password",placeholder="sk-proj-bj1imSfsrYJVabH2sdfasd22AFf")

api_key_button=st.sidebar.button("Done ⤤",key="api_key")
if api_key_button:
    if user_api_key:
        try:
            # Test the API key by making a simple request
            test_client = openai.OpenAI(api_key=user_api_key)
            test_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            st.session_state['API_Key'] = user_api_key
            st.success("API key validated successfully!")
            st.balloons()
        except Exception as e:
            st.error("Invalid API key. Please check your key and try again.")
            st.session_state['API_Key'] = None
    else:
        st.warning("Please enter an API key first!")

demo_api_key=st.sidebar.button("Use Demo Api Key ⤤", key="demo_api_key" )
if demo_api_key:
    st.session_state['API_Key'] = api_key_streamlit_secrets
    st.session_state['is_demo_key'] = True
    st.session_state['trial_count'] = 0
    st.success("Demo API key activated! You have 5 trials remaining.")
    st.balloons()

st.sidebar.text('----------------------------------')

summarizer_button = st.sidebar.button("Use Summarizer Tool ⤤",key="summarizer")
if summarizer_button:
    summarise_placeholder = st.sidebar.write("Nice chatting with you my friend ❤️:\n\n"+st.session_state['conversation'].memory.buffer)

# ------ Main Page Design and Code
st.markdown(
    "<h1 style='text-align: center; font-size: 25px;'> How Can I Assist You 🖳  </h1>",
    unsafe_allow_html=True
)
respose_container= st.container()
input_container= st.container()

with input_container:
    with  st.form(key="my_from",clear_on_submit=True):
        user_question=st.text_area ("Chat With Me •‿• ", key="input",height=70)
        submit_button=st.form_submit_button(label="Submit ⤤")
        if submit_button:
            if not st.session_state['API_Key']:
                st.warning("Please enter your API key or use the demo API key first!")
            else:
                if st.session_state['is_demo_key']:
                    if st.session_state['trial_count'] >= 5:
                        st.error("You have used all your demo trials. Please enter your own API key to continue.")
                    else:
                        st.session_state['trial_count'] += 1
                        st.session_state['messages'].append(user_question)
                        answer = UserInput_Click(user_question,st.session_state['API_Key'])
                        st.session_state['messages'].append(answer)
                        st.info(f"Trials remaining: {5 - st.session_state['trial_count']}")
                else:
                    st.session_state['messages'].append(user_question)
                    answer = UserInput_Click(user_question,st.session_state['API_Key'])
                    st.session_state['messages'].append(answer)

            with respose_container:
                for i in range(len(st.session_state['messages'])):
                        if (i % 2) == 0:
                            message(st.session_state['messages'][i], is_user=True, key=str(i) + '_user')
                        else:
                            message(st.session_state['messages'][i], key=str(i) + '_AI')
                            
    
# st.sidebar.text("Develop with ❤ By Shams")
