"""
Streamlit page for neural search.
"""

import streamlit as st
from openai import BadRequestError

from src import components
from src.entities import Avatar, Message
from src.genai import ask_model

if not (messages := st.session_state["history"]):
    # display a welcome alert at the beginning
    components.add_welcome_alert("ask")
else:
    # display message history
    for message in messages:
        with st.chat_message(name=message.role, avatar=message.icon):
            st.write(message.content)

# wait for a user message
components.add_chat_input()
if not (user_message := st.session_state.get("user_message")):
    st.stop()

# display the user message
with st.chat_message("user", avatar=Avatar.USER):
    st.markdown(user_message)

# stream the model response
with st.chat_message("assistant", avatar=Avatar.ASSISTANT):
    try:
        stream = ask_model(user_message, messages, st.session_state["contexts"])
    except BadRequestError as e:
        # logging.warning(e.body["message"])
        message = """Your message has triggered a content filter. This may be either an accidental
        false positive, in which case you should rephrase your message and try again, or due to a
        malicious intent, in which  case you have violated the terms of use."""
        stream = (x for x in message)
    except Exception:
        message = "Unknown error has occurred. Contact us to report this issue."
        stream = (x for x in message)
    assistant_response = st.write_stream(stream)

# save the messages, keeping only the last 10 messages
history = st.session_state["history"]
history.extend(
    [
        Message(role="user", content=user_message),
        Message(role="assistant", content=assistant_response),
    ]
)
st.session_state["history"] = history[-10:]
