import streamlit as st
import googleapiclient.discovery
import os
import requests
from streamlit_option_menu import option_menu
from textblob import TextBlob
from datetime import datetime
import pandas as pd
import numpy as np
from googleapiclient.discovery import build
start_time = datetime(year=2020, month=10, day=1).strftime('%Y-%m-%dT%H:%M:%SZ')
end_time = datetime(year=2021, month=5, day=11).strftime('%Y-%m-%dT%H:%M:%SZ')
st.markdown(f"<h1 style='text-align: center; color: Tomato;'>Best Video Prediction</h1>", unsafe_allow_html=True)
def rankFinder(comment):
    list_1 = []
    for ele in comment:
        t=TextBlob(ele)
        list_1.append(t.sentiment.polarity)
        if len(list_1)>0:
            return abs(sum(list_1)/len(list_1))
        else:
            pass
s=[]
ids=[]
ind=[]
api_key="AIzaSyApIE8uHcg1wcDZZNCPEY4qWSwxRifBQ8w"
ine=st.text_input("Enter a topic")
youtube=build('youtube','v3',developerKey=api_key)
results = youtube.search().list(q=ine, part="snippet", type="video", order="viewCount",publishedAfter=start_time,
                            publishedBefore=end_time, maxResults=5).execute()
for item in sorted(results['items'], key=lambda x:x['snippet']['publishedAt']):
    coll = item['snippet']['title'], item['id']['videoId']
    df_1 = pd.DataFrame(coll)
    for i in range(len(df_1)):
        s.append(df_1.iloc[i,0])
for j in range(0,len(s),2):
    ind.append(s[j])
for i in range(1,len(s),2):
    ids.append(s[i])
for it in range(0,len(ids)):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = api_key)
    request = youtube.commentThreads().list(
        part="id,snippet",
        maxResults=100,
        order="relevance",
        videoId= ids[it]
    )
    response = request.execute()
    authorname = []
    comments = []
    positive = []
    negative = []
    for i in range(len(response["items"])):
        authorname.append(response["items"][i]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"])
        comments.append(response["items"][i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
        df_1 = pd.DataFrame(comments, index = authorname,columns=["Comments"])
    for i in range(len(df_1)):
        text =  TextBlob(df_1.iloc[i,0])
        polarity = text.sentiment.polarity
        if polarity>0:
            positive.append(df_1.iloc[i,0])
        elif polarity<0:
            negative.append(df_1.iloc[i,0])
        else:
            pass
    inh="https://www.youtube.com/watch?v="
    inh+=ids[it]
    if len(negative)==0:
        rank_1 = rankFinder(positive)
        inten_1=rank_1*len(positive)
        neg_int=0
        pos_int= 1/(1 + np.exp(-inten_1))
        if pos_int>=0.95:
            st.markdown(f"<h3 style='color: green;'>{ind[it]}</h3>", unsafe_allow_html=True)
            st.write(inh)
            st.write("⭐⭐⭐⭐⭐")
        if pos_int>0.75 and pos_int<0.95:
            st.markdown(f"<h3 style='color: green;'>{ind[it]}</h3>", unsafe_allow_html=True)
            st.write(inh)
            st.write("⭐⭐⭐⭐✰")
        if pos_int>0.50 and pos_int<0.75:
            st.markdown(f"<h3 style='color: orange;'>{ind[it]}</h3>", unsafe_allow_html=True)
            st.write(inh)
            st.write("⭐⭐⭐✰✰")
        if pos_int>0.30 and pos_int<0.50:
            st.markdown(f"<h3 style='color: red;'>{ind[it]}</h3>", unsafe_allow_html=True)
            st.write(inh)
            st.write("⭐⭐✰✰✰")
        if pos_int<0.30:
            st.markdown(f"<h3 style='color: red;'>{ind[it]}</h3>", unsafe_allow_html=True)
            st.write(inh)
            st.write("⭐✰✰✰✰")
    if len(negative)>0:
        rank_1 = rankFinder(positive)
        inten_1=rank_1*len(positive)
        rank_2=rankFinder(negative)
        inten_2=rank_2*len(negative)
        pos_int=inten_1/(inten_1+inten_2)
        neg_int=inten_2/(inten_1+inten_2)
        if pos_int>=0.95:
            st.markdown(f"<h3 style='color: green;'>{ind[it]}</h3>", unsafe_allow_html=True)
            st.write(inh)
            st.write("⭐⭐⭐⭐⭐")
        if pos_int>0.75 and pos_int<0.95:
            st.markdown(f"<h3 style='color: green;'>{ind[it]}</h3>", unsafe_allow_html=True)
            st.write(inh)
            st.write("⭐⭐⭐⭐✰")
        if pos_int>0.50 and pos_int<0.75:
            st.markdown(f"<h3 style='color: orange;'>{ind[it]}</h3>", unsafe_allow_html=True)
            st.write(inh)
            st.write("⭐⭐⭐✰✰")
        if pos_int>0.30 and pos_int<0.50:
            st.markdown(f"<h3 style='color: red;'>{ind[it]}</h3>", unsafe_allow_html=True)
            st.write(inh)
            st.write("⭐⭐✰✰✰")
        if pos_int<0.30:
            st.markdown(f"<h3 style='color: red;'>{ind[it]}</h3>", unsafe_allow_html=True)
            st.write(inh)
            st.write("⭐✰✰✰✰")
    st.markdown(f"<hr/>",unsafe_allow_html=True)
