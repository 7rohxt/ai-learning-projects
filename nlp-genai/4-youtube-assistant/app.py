import streamlit as st
import youtube_helper as yth
import textwrap
import os

st.title("🎥 YouTube Assistant")

with st.sidebar:
    st.header("Video & Question")
    with st.form(key="youtube_form"):
        youtube_url = st.text_area("YouTube video URL", max_chars=200)
        query = st.text_area("Ask a question about the video", max_chars=200)
        openai_api_key = st.text_input("OpenAI API Key", type="password")
        submit_button = st.form_submit_button(label="Submit")

if submit_button:
    if not youtube_url.strip():
        st.error("Please provide a YouTube video URL.")
    elif not query.strip():
        st.error("Please enter a question.")
    elif not openai_api_key.strip():
        st.error("Please enter your OpenAI API key.")
    else:
        # Set API key for OpenAI
        os.environ["OPENAI_API_KEY"] = openai_api_key
        
        with st.spinner("Processing the video..."):
            db = yth.create_db_from_youtube_video_url(youtube_url)
            response = yth.get_response_from_query(db, query)
        
        st.subheader("Question")
        st.write(textwrap.fill(query, width=85))

        st.subheader("Answer")
        st.write(textwrap.fill(response, width=85))