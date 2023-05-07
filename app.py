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

with st.container():
    st.title("Chat with Claude")
    st.markdown("Welcome to our chat application!")

with st.container():
    # Display the entire conversation
    for i, prompt in enumerate(st.session_state.prompts):
        if prompt['role'] == 'Human' and i != 0:
            st.write(f"You: {prompt['content']}")
        elif prompt['role'] == 'Assistant':
            st.write(f"Claude: {prompt['content']}")

with st.container():
    with st.form(key='message_form'):
        user_topic = st.text_input("Enter the topic for the class:", key="user_topic")  # add this line
        submit_button = st.form_submit_button(label='Send')
        
        if submit_button:
            if user_topic:
                company_purpose = "Our purpose is to make Web3 accessible to everyone, irrespective of their technical background."
                st.session_state.prompts.append({
                    "role": "Human",
                    "content": f"""You are a seasoned teacher with the goal to impact your students allowing them to understand and engage. As an AI developed by Kravata, a company with the purpose of '{company_purpose}', I need you to generate a structure for a class on the topic of '{user_topic}'. The class should be aimed at beginners in the field of Web3. Please remember to use simple, easy-to-understand language and provide a clear outline of the class with key learning points. Keep the class short and impactful."""
                })

            if st.session_state.prompts:
                with st.spinner('Waiting for Claude...'):
                    try:
                        result = send_message(st.session_state.prompts)

                        # Append Claude's response to the prompts
                        st.session_state.prompts.append({
                            "role": "Assistant",
                            "content": result['completion']
                        })

                        # Rerun the script to update the chat
                        st.experimental_rerun()

                        # Display a success message
                        st.success("Message sent successfully!")

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

with st.container():
    if st.button('Restart'):
        st.session_state.prompts = []
        st.experimental_rerun()