import streamlit as st

# Import the SessionState module
from streamlit.report_thread import get_report_ctx
from streamlit.hashing import _CodeHasher
from streamlit.server.server import Server

class _SessionState:
    def __init__(self, **kwargs):
        """A new SessionState object."""
        for key, val in kwargs.items():
            setattr(self, key, val)


def get_session_state(**kwargs):
    """Gets a SessionState object for the current session.
    Creates a new object if necessary."""
    ctx = get_report_ctx()
    session_id = ctx.session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")

    this_session = session_info.session

    if not hasattr(this_session, "_custom_session_state"):
        this_session._custom_session_state = _SessionState(**kwargs)

    return this_session._custom_session_state


def generate_content(topic, company_purpose):
    # Prepare the prompt for Claude
    prompt = f"""
    You are a seasoned teacher with the goal to impact your students, allowing them to understand and engage with the topic of {topic}. You are inspired by the purpose of the company, which is "{company_purpose}". Please provide a proposed structure for the class.
    """
    # Here you would call the function to send the prompt to Claude and get the response
    # For now, let's return the prompt for testing
    return prompt

st.title("Content Generator for Kravata Academy")

# Get the session state
session_state = get_session_state(conversation=[])

# Get the topic from the user
topic = st.text_input("Enter the topic for the class:")
company_purpose = "Educate audiences and position Kravata as the 'web3 for all' company."

if st.button("Generate Content"):
    content = generate_content(topic, company_purpose)
    # Add the content to the conversation history
    session_state.conversation.append(content)
    
    # Display the conversation history
    for i, message in enumerate(session_state.conversation):
        st.write(f"Message {i + 1}: {message}")
