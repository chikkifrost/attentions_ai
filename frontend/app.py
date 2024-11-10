# frontend/app.py

import streamlit as st
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Academic Research Paper Assistant", layout="wide")
st.title("📚 Academic Research Paper Assistant")

# Initialize session state variables
if 'topic' not in st.session_state:
    st.session_state['topic'] = ''
if 'question' not in st.session_state:
    st.session_state['question'] = ''
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Sidebar for topic input
st.sidebar.header("Search for Research Papers")
st.session_state['topic'] = st.sidebar.text_input("Enter Research Topic:", key='topic_input')

if st.sidebar.button("Search Papers", key='search_button'):
    topic = st.session_state['topic']
    if not topic.strip():
        st.sidebar.error("Please enter a valid research topic.")
    else:
        with st.spinner('Fetching and storing papers...'):
            try:
                response = requests.post(f"{API_URL}/collect_papers/", json={"topic": topic})
                response.raise_for_status()
                st.sidebar.success(response.json()["message"])
            except requests.exceptions.RequestException as e:
                st.sidebar.error(f"Error: {e}")

# Display Papers
topic = st.session_state['topic']
if topic:
    st.header(f"Papers related to '{topic}'")

    # Fetch papers from backend
    try:
        response = requests.post(f"{API_URL}/get_papers/", json={"topic": topic})
        response.raise_for_status()
        papers = response.json()["papers"]

        for paper in papers:
            st.subheader(paper['title'])
            st.write(f"**Authors:** {', '.join(paper['authors'])}")
            st.write(f"**Published:** {paper['published']}")
            st.write(paper['summary'])
            st.write(f"[PDF Link]({paper['pdf_url']})")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch papers: {e}")

    # Generate Review Paper
    st.subheader("Generated Review Paper")
    if st.button("Generate Review Paper", key='generate_review_button'):
        with st.spinner('Generating review paper...'):
            try:
                response = requests.post(f"{API_URL}/generate_review/", json={"topic": topic})
                response.raise_for_status()
                review = response.json()["review_paper"]
                st.text_area("Review Paper", review, height=300)
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to generate review paper: {e}")

    # Future Works
    st.subheader("Future Research Opportunities")
    if st.button("Generate Future Works", key='future_works_button'):
        with st.spinner('Generating future works...'):
            try:
                response = requests.post(f"{API_URL}/generate_future_works/", json={"topic": topic})
                response.raise_for_status()
                future_works = response.json()["future_works"]
                st.write(future_works)
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to generate future works: {e}")

    # Chat Interface
    st.subheader("Ask Questions about the Papers")
    st.session_state['question'] = st.text_input("Enter your question:", key='question_input')
    if st.button("Ask", key='ask_button'):
        user_question = st.session_state['question']
        if not user_question.strip():
            st.error("Please enter a valid question.")
        else:
            with st.spinner('Processing your question...'):
                try:
                    response = requests.post(
                        f"{API_URL}/answer_question/",
                        json={"topic": topic, "question": user_question}
                    )
                    response.raise_for_status()
                    answer = response.json()["answer"]
                    references = response.json().get("references", [])
                    st.write(f"**Answer:** {answer}")
                    if references:
                        st.write("**References:**")
                        for ref in references:
                            st.write(f"- {ref}")
                    # Save chat history
                    st.session_state['chat_history'].append({
                        'question': user_question,
                        'answer': answer,
                        'references': references
                    })
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to get answer: {e}")

    # Display Chat History
    if st.session_state['chat_history']:
        st.subheader("Chat History")
        for idx, chat in enumerate(st.session_state['chat_history']):
            st.write(f"**Question {idx+1}:** {chat['question']}")
            st.write(f"**Answer:** {chat['answer']}")
            if chat['references']:
                st.write("**References:**")
                for ref in chat['references']:
                    st.write(f"- {ref}")
            st.write("---")