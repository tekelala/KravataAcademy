import streamlit as st
from streamlit import caching

@st.cache(allow_output_mutation=True)
def get_conversation():
    return []

def generate_content(topic, company_purpose):
    prompt = f"""
    You are a seasoned teacher with the goal to impact your students, allowing them to understand and engage with the topic of {topic}. You are inspired by the purpose of the company, which is "{company_purpose}". Please provide a proposed structure for the class.
    """
    return prompt

st.title("Content Generator for Kravata Academy")

# Get the topic from the user
topic = st.text_input("Enter the topic for the class:")
company_purpose = "Educate audiences and position Kravata as the 'web3 for all' company."

if st.button("Generate Content"):
    # Get the conversation history
    conversation = get_conversation()

    # Generate new content and add it to the conversation history
    content = generate_content(topic, company_purpose)
    conversation.append(content)
    
    # Display the conversation history
    for i, message in enumerate(conversation):
        st.write(f"Message {i + 1}: {message}")
