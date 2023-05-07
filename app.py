import streamlit as st

def generate_content(topic, company_purpose):
    # Prepare the prompt for Claude
    prompt = f"""
    You are a seasoned teacher with the goal to impact your students, allowing them to understand and engage with the topic of {topic}. You are inspired by the purpose of the company, which is "{company_purpose}". Please provide a proposed structure for the class.
    """
    # Here you would call the function to send the prompt to Claude and get the response
    # For now, let's return the prompt for testing
    return prompt

st.title("Content Generator for Kravata Academy")

topic = st.text_input("Enter the topic for the class:")
company_purpose = "Educate audiences and position Kravata as the 'web3 for all' company."

if st.button("Generate Content"):
    content = generate_content(topic, company_purpose)
    st.write(content)
