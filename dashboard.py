import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

# Set config at the top
st.set_page_config(page_title="YouTube Trending Dashboard", layout="wide")

# Load Data
@st.cache_data(ttl=300)  # refresh every 5 minutes
def load_data():
    df = pd.read_csv("realtime_trending.csv")
    df['published_at'] = pd.to_datetime(df['published_at'])
    return df

df = load_data()

# Header
st.title("📈 Real-Time YouTube Trending Dashboard")
st.markdown("Visualize the latest trending YouTube videos and track their engagement over time.")
st.markdown("---")

# Top 10 Trending Videos
st.subheader("🔥 Top 10 Trending Videos Right Now")

top_10 = df.sort_values(by='views', ascending=False).drop_duplicates('video_id').head(10)
selected_title = st.selectbox("🎬 Click a title to see view trends", top_10['title'])

# Display video metadata
selected_row = top_10[top_10['title'] == selected_title].iloc[0]
st.markdown(f"**Channel:** {selected_row['channel']}  |  **Views:** {selected_row['views']}  |  **Likes:** {selected_row['likes']}")

# Chart for views over time of that video
video_id = selected_row['video_id']
video_df = df[df['video_id'] == video_id].sort_values('published_at')

line_chart = alt.Chart(video_df).mark_line(point=True).encode(
    x=alt.X('published_at:T', title='Time'),
    y=alt.Y('views:Q', title='Views'),
    tooltip=['published_at:T', 'views']
).properties(
    width=800,
    height=400,
    title=f"📊 Views Over Time for '{selected_title}'"
).configure_axis(
    labelColor='steelblue',
    titleColor='steelblue'
).configure_title(
    color='steelblue'
)

st.altair_chart(line_chart)

# Footer
st.markdown("---")
st.markdown("👨‍💻 Built with ❤️ by **Pandy keerthika**")
