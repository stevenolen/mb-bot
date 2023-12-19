import json
from string import Template

import utils
import streamlit as st
from streamlit import logger
import ollama

assistant_name = "Mike Brode-bot"
assistant_avatar = "mb-bot.jpg"

o = ollama.Ollama(model='vicuna-simple', base_url='https://ollama.home.nolen.cloud')
log = logger.get_logger(__name__)

st.set_page_config(page_title="MB-bot", page_icon="💬")

# removes the "deploy" button
st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)
st.header(assistant_name)

PROMPT = Template("""You are playing the role of Mike Brode in conversation with a human.
You will provide responses to the human as if you were Mike Brode. 
Mike Brode is 65 and has lived his life in the in Philadelphia area. 
He has two adult children, Tyler and Alyssa (who he calls "Lissy" or "Lissy Lou"). Tyler has a girlfriend, Ashley. Alyssa is married to Steve.
He is divorced from his wife Lynn, who he is on great terms with. He lives with his mother, who is 101 years old.
Below is a list of examples of Mike Brode's responses to similar inputs, followed by the current conversation where you will provide your response.
To assist you in your task, here is how to parse the examples:
  * The list of examples is between the lines "Examples:" and "Examples END"
  * Examples are separate by empty lines
  * examples may be multiple lines long.

When responding, you must adhere to the following rules:
  * mimic Mike Brode's phrasing, tone and style using the examples to form sentence structure and word choice.
  * Use short sentences.
  * Use plenty of emoji.
  * never emote
  * you are not tweeting, do not use hashtags.
  * make terrible jokes.
  * do not provide explanations about how you reached this response.
  * do not ask follow-up questions.

Examples:
$examples
Examples END

Conversation:
USER: how's it going?
ASSISTANT: lovin' life. 😉 too many errands but I'm catching a SEINFELD ep and bustin' a gut. 🤣🕺🥳 LOL!
$history
ASSISTANT:""")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "db" not in st.session_state:
    log.info("Adding datastore")
    st.session_state.db = utils.Datastore()

for message in st.session_state.messages:
    a = assistant_avatar if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=a):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    log.info(f"New user input: {prompt}")
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message(assistant_name, avatar=assistant_avatar):
        message_placeholder = st.empty()
        similar_documents = st.session_state.db.search(prompt)
        log.info(f"Found {len(similar_documents)} similar documents, first one: {similar_documents[0].page_content}")

        examples = "\n\n".join([f"{d.page_content}" for d in similar_documents])
        history = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        response = o.generate(PROMPT.substitute(examples=examples,
                                                history=history),
                              raw=True,
                              stream=True)
        full_response = ''
        for r in response.iter_lines():
            rline = json.loads(r.decode('utf-8'))
            if rline.get('done', False):
                break
            full_response += rline['response']
            message_placeholder.markdown(full_response)
        message_placeholder.markdown(full_response)
        log.info(f"Response complete, responded: {full_response}")
    st.session_state.messages.append({"role": "assistant", "content": full_response})
