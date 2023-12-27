import streamlit as st
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
import time
import re

client = OpenAI()

full_text = ""

link_inserted = False

app_title = st.title(":red[YouTube] Video Summarizer")
text_input = st.text_input(label="", placeholder="Enter a YouTube Link")
st.text("")

link_inserted = st.button("Summarize", type="primary")

if link_inserted:

    with st.spinner('Summarizing YouTube Video...'):

        time.sleep(3)

        resp = ""

        try:
            data = { 'url': text_input }
            resp = YouTubeTranscriptApi.get_transcript(data['url'].split("v=")[-1])

        except:
            st.error("Not a valid YouTube URL.")

        if resp:

            full_transcript = " ".join([element["text"] for element in resp])

            system_prompt = "I want you to act as a Youtuber explaining a video for me. I want you to provide three sections all in one go. Do not include headers for each section. For each section, do not include titles. Here is the tutorial I want you to summarize: '" + full_transcript + "'"
            prompt = "Section 1: Give me a good title summarizing what the video is about!. Make sure to start this section with [PART_1]. Section 2: Give me a brief summary! Start this section with [PART_2]. Section 3: Give me a list of numbered items detailing important topics of the video and add sub bullet points explaining each point. Start the response with [PART_3]. Do not have a header"

            completion = client.chat.completions.create(

                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': prompt}
                ],
                model="gpt-3.5-turbo",
            )

            full_text = completion.choices[0].message.content

        while not full_text and resp:
            time.sleep(3)

    if full_text:
        st.success('Done!')

if full_text:

    title = full_text.split('[PART_1]')[1].split('[PART_2]')[0].strip()

    st.header(title)

    st.subheader("Brief Summary:")

    summary = full_text.split('[PART_2]')[1].split('[PART_3]')[0].strip()

    st.write(summary)

    action_items = full_text.split('[PART_3]')[1].strip()

    st.subheader("Important Topics:")

    st.write(action_items)
