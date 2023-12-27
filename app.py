import streamlit as st
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
import time
import re


full_text = ""

app_title = st.title(":red[YouTube] Video Summarizer")

text_input = st.text_input(label="", placeholder="Enter a YouTube Link")
st.text("")

link_inserted = st.button("Summarize", type="primary")

if link_inserted:

    with st.spinner("Summarizing YouTube Video..."):
        time.sleep(3)

        resp = ""
        full_transcript = ""

        try:
            data = { "url": text_input }
            resp = YouTubeTranscriptApi.get_transcript(data['url'].split("v=")[-1])

        except:
            st.error("Not a valid YouTube URL.")

        if resp:

            full_transcript = "".join([element["text"] for element in resp])

        while not full_transcript:
            time.sleep(3)

    if full_transcript:
        st.success('Done!')

    if full_transcript:

        st.write(full_transcript)
