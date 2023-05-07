import streamlit as st
import requests
import json

def send_message(prompts):
    api_url = "https://api.anthropic.com/v1/complete"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": st.secrets["API_KEY"]  # Use the API key from Streamlit's secrets
    }

    # Prepare the prompts for Claude
    conversation = "\n\n".join([f'{item["role"]}: {item["content"]}' for item in prompts]) + "\n\nAssistant:"

    # Define the body of the request
    body = {
        "prompt": conversation,
        "model": "claude-v1.3",
        "max_tokens_to_sample": 500,
        "stop_sequences": ["\n\nHuman:"]
    }

    # Make a POST request to the Claude API
    response = requests.post(api_url, headers=headers, data=json.dumps(body))
    response.raise_for_status()

    return response.json()

# Initialize session state variables
if "prompts" not in st.session_state:
    st.session_state.prompts = []

if "class_generated" not in st.session_state:
    st.session_state.class_generated = False

# Container 1: Title and banner image
with st.container():
    st.title("Chat with the Kravata Teacher")
    st.markdown("Welcome to the class designer!")

# Container 2: Enter the topic for the class
with st.container():
    if not st.session_state.class_generated:
        with st.form(key='message_form'):
            user_topic = st.text_input("Enter the topic for the class:", key="user_topic")  
            submit_button = st.form_submit_button(label='Send')
            
            if submit_button and user_topic:
                company_purpose = "Our purpose is to make Web3 accessible to everyone, irrespective of their technical background."
                st.session_state.prompts.append({
                    "role": "Human",
                    "content": f"""You are a seasoned teacher with the goal to impact your students allowing them to understand and engage. As an AI developed by Kravata, a company with the purpose of '{company_purpose}', I need you to generate a structure for a class on the topic of '{user_topic}'. The class should be aimed at beginners in the field of Web3. Please remember to use simple, easy-to-understand language and provide a clear outline of the class with key learning points. Keep the class short and impactful."""
                })
# Container 3: Show the answer by Claude
with st.container():
    if st.session_state.prompts and user_topic and submit_button:
        with st.spinner('Waiting for the Kravata Teacher...'):
            try:
                result = send_message(st.session_state.prompts)

                # Append Claude's response to the prompts
                st.session_state.prompts.append({
                    "role": "Assistant",
                    "content": result['completion']
                })

                # Display a success message
                st.success("Message sent successfully!")

                # Mark the class as generated only if there was a user message
                if submit_button and user_topic:
                    st.session_state.class_generated = True

                # Display the entire conversation
                for i, prompt in enumerate(st.session_state.prompts):
                    if prompt['role'] == 'Human' and i != 0:
                        st.write(f"You: {prompt['content']}")
                    elif prompt['role'] == 'Assistant':
                        st.write(f"Kravata Teacher: {prompt['content']}")

            except requests.exceptions.HTTPError as errh:
                st.error(f"HTTP Error: {errh}")
            except requests.exceptions.ConnectionError as errc:
                st.error(f"Error Connecting: {errc}")
            except requests.exceptions.Timeout as errt:
                st.error(f"Timeout Error: {errt}")
            except requests.exceptions.RequestException as err:
                st.error(f"Something went wrong: {err}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

# Container 4: Reset button
with st.container():
    if st.button('Reset'):
        st.session_state.prompts = []
        st.session_state.class_generated = False

# Container 5: Which part of the class do you want to develop
with st.container():
    if st.session_state.class_generated:
        with st.form(key='message_form'):
            user_message = st.text_input("Which part of the class do you want to develop?", key=f"user_input_{len(st.session_state.prompts)}")
            submit_button = st.form_submit_button(label='Send')

            if submit_button and user_message:
                st.session_state.prompts.append({
                    "role": "Human",
                    "content": user_message
                })
                # Re-run the script after appending new user_message to prompts
                st.experimental_rerun()
