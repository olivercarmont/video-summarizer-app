# YouTube Video Summarizer App 🎥

> **About Myself**: 🤖 I'm an aspiring ML Engineer sharing my learnings on ML/AI on [**YouTube!**](https://www.youtube.com/@olivercarmont) <br />

## Overview:
Welcome to this video tutorial on creating a YouTube Video Summarizer app using Python, Streamlit, YouTube Transcript API, and OpenAI's GPT-3.5 Turbo. If you prefer video format, check out the [**YouTube tutorial**](https://www.youtube.com/watch?v=p1xBjx6rnmA&t=984s&ab_channel=OliverCarmont).
<br />

## 1 - Setting Up Your Project:
1. Open your terminal and navigate to your desktop.
2. Create a new project folder, e.g., `youtube-summarizer`.
3. Inside the folder, create an app.py file with:`touch app.py`.

## 2 - Adding OpenAI API Key to .env:
1. Obtain your OpenAI API key from [OpenAI API](https://platform.openai.com/signup).
2. In Terminal, inside your project directory, add an environment variable by running: `export OPENAI_API_KEY=(your api key here)`

## 3 - Install Dependencies
1. Install the following dependecies
```python
# Install Streamlit
!pip install streamlit

# Install YouTube Transcript API
!pip install youtube_transcript_api

# Install OpenAI library
!pip install openai
```

## 4 - Import Libraries
1. Inside app.py import the following libraries:

```python
import streamlit as st
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
import time
import re
```

## 5 - Initialize Variables
1. In the same file, initialize the following variables:

```python
client = OpenAI() # Initialize OpenAI Client
full_text = ""
link_inserted = False
```

## 6 - Create Streamlit Dashboard
1. Add the following code below to add a nice dashboard to our app:

```python
# Create Streamlit App Title
app_title = st.title(":red[YouTube] Video Summarizer")

# Create Text Input for YouTube Link
text_input = st.text_input(label="", placeholder="Enter a YouTube Link")

# Add Space
st.text("")

# Create Summarize Button
link_inserted = st.button("Summarize", type="primary")
```

## 7 - Test The App
1. Activate your virtual environment (if using one).
2. Run the Streamlit app: `streamlit run app.py`.
3. Input a YouTube link and click "Summarize."


## 8 - Summarize YouTube Video
1. Add logic to transcribe video with YouTubeTranscriptAPI and summarize it with OpenAI's gpt-3.5-turbo.
   
```python
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
```


## 9 - Display Video Summary
1. Write the following logic at the bottom of the file to display the video summary.
```python
if full_text:
    title = full_text.split('[PART_1]')[1].split('[PART_2]')[0].strip()
    st.header(title)
    st.subheader("Brief Summary:")
    summary = full_text.split('[PART_2]')[1].split('[PART_3]')[0].strip()
    st.write(summary)
    action_items = full_text.split('[PART_3]')[1].strip()
    st.subheader("Important Topics:")
    st.write(action_items)
```

### That's it! 🎊
Hope you found this tutorial useful. Make sure to subscribe to my [**YouTube channel**](https://www.youtube.com/@olivercarmont) for more updates!
