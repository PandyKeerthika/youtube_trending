import streamlit as st
import pandas as pd
import altair as alt
import time

# Load the dataset
df = pd.read_csv('realtime_trending.csv')

# Preprocess and clean the data
df['published_date'] = pd.to_datetime(df['published_at'])
df['views'] = df['views'].apply(pd.to_numeric, errors='coerce')
df['likes'] = df['likes'].apply(pd.to_numeric, errors='coerce')

# Set page config with friendly theme and wider layout
st.set_page_config(page_title="Real-Time YouTube Trending", page_icon="📈", layout="wide")

# Custom styling for clean, modern interface
st.markdown("""
    <style>
    .reportview-container {
        background-color: #f0f8ff;
    }
    .sidebar .sidebar-content {
        background-color: #4f8ea6;
    }
    .stButton>button {
        background-color: #4f8ea6;
        color: white;
        border-radius: 8px;
    }
    .stTextInput>input {
        border-radius: 8px;
        border: 2px solid #4f8ea6;
    }
    .stSelectbox>div {
        background-color: #e0f7fa;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.title("📊 Real-Time YouTube Trending Dashboard")
st.markdown("""
This dashboard helps creators track and analyze **trending videos** on YouTube in real-time. 
Use the filters below to explore the trends and insights.
""")

# --- AUTO-REFRESH every 5 minutes ---

# Initialize a variable to auto-refresh every 5 minutes (300 seconds)
st.cache(ttl=300)  # Cache the data for 5 minutes

# Metrics Section (Will auto-refresh)
col1, col2, col3 = st.columns(3)
col1.metric("🎥 Total Videos", f"{len(df):,}")
col2.metric("📺 Unique Channels", f"{df['channel'].nunique():,}")
col3.metric("📈 Max Views", f"{df['views'].max():,}")

# Section Divider
st.markdown("---")

# Filter Section: Select by Date Range
st.subheader("📆 Filter by Date Range")
date_range = st.slider("Select Date Range", 
                       min_value=df['published_date'].min().date(), 
                       max_value=df['published_date'].max().date(),
                       value=(df['published_date'].min().date(), df['published_date'].max().date()))

filtered_df = df[(df['published_date'].dt.date >= date_range[0]) & (df['published_date'].dt.date <= date_range[1])]

# Filter Section: Select Channel
channels = df['channel'].unique()
selected_channel = st.selectbox("🔍 Filter by Channel", options=["All"] + list(channels))

if selected_channel != "All":
    filtered_df = filtered_df[filtered_df['channel'] == selected_channel]

# Filter Section: Keyword Search
keyword = st.text_input("🔎 Filter by Keyword in Title", placeholder="Enter keyword to filter videos")
if keyword:
    filtered_df = filtered_df[filtered_df['title'].str.contains(keyword, case=False)]

# Section Divider
st.markdown("---")

# Insights Section: Top 10 Trending Channels
st.subheader("🏆 Top 10 Trending Channels")
top_channels = filtered_df['channel'].value_counts().nlargest(10)
st.bar_chart(top_channels)

# Section Divider
st.markdown("---")

# Trend Over Time (Line Chart)
st.subheader("📈 Views Over Time")
views_by_day = filtered_df.groupby('published_date')['views'].sum().reset_index()

chart = alt.Chart(views_by_day).mark_line(point=True).encode(
    x='published_date:T',
    y='views:Q',
    tooltip=['published_date:T', 'views:Q']
).properties(height=300)
st.altair_chart(chart, use_container_width=True)

# Section Divider
st.markdown("---")

# Download Filtered Data
st.subheader("📥 Download Filtered Data")
st.download_button("Download Filtered Data (CSV)", 
                   data=filtered_df.to_csv(index=False), 
                   file_name="filtered_trending_videos.csv",
                   mime='text/csv')

# Footer Section
st.markdown("---")
st.caption("Created with ❤️ by Your Name")

