import streamlit as st
import googleapiclient.discovery
import os
import requests
from streamlit_option_menu import option_menu
from textblob import TextBlob
import pandas as pd
import numpy as np
from apiclient.discovery import build
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
api_key="AIzaSyDHuMMpAmSYWe_uYwv0ra2S7FgA94Zhmd0"
ine=st.text_input("Enter a topic")
youtube=build('youtube','v3',developerKey=api_key)
results=youtube.search().list(q=ine,part="snippet",type="video",
order="viewCount").execute()
for item in sorted(results['items'], key=lambda x:x['snippet']['publishedAt']):
    coll = item['snippet']['title'], item['id']['videoId']
    df_1 = pd.DataFrame(coll)
    for i in range(len(df_1)):
        s.append(df_1.iloc[i,0])
for i in range(1,len(s),2):
    ids.append(s[i])
for it in ids:
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = api_key)
    request = youtube.commentThreads().list(
        part="id,snippet",
        maxResults=100,
        order="relevance",
        videoId= it
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
    inh+=it
    if len(negative)==0:
        rank_1 = rankFinder(positive)
        inten_1=rank_1*len(positive)
        neg_int=0
        pos_int= 1/(1 + np.exp(-inten_1))
        if pos_int>=0.95:
            st.subheader(inh)
            st.write("5")
        if pos_int>0.75 and pos_int<0.95:
            st.subheader(inh)
            st.write("4")
        if pos_int>0.50 and pos_int<0.75:
            st.subheader(inh)
            st.write("3")
        if pos_int>0.30 and pos_int<0.50:
            st.subheader(inh)
            st.write("2")
        if pos_int<0.30:
            st.subheader(inh)
            st.write("1")
    if len(negative)>0:
        rank_1 = rankFinder(positive)
        inten_1=rank_1*len(positive)
        rank_2=rankFinder(negative)
        inten_2=rank_2*len(negative)
        pos_int=inten_1/(inten_1+inten_2)
        neg_int=inten_2/(inten_1+inten_2)
        if pos_int>=0.95:
            st.subheader(inh)
            st.write("5")
        if pos_int>0.75 and pos_int<0.95:
            st.subheader(inh)
            st.write("4")
        if pos_int>0.50 and pos_int<0.75:
            st.subheader(inh)
            st.write("3")
        if pos_int>0.30 and pos_int<0.50:
            st.subheader(inh)
            st.write("2")
        if pos_int<0.30:
            st.subheader(inh)
            st.write("1")
    st.markdown(f"<hr/>",unsafe_allow_html=True)