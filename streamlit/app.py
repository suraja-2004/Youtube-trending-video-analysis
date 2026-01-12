import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="YouTube Trending Dashboard",
    page_icon="📊",
    layout="wide"
)

# ----------------------------
# Load Data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("youtube.csv")
    return df

df = load_data()

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("🔎 Filter Options")

category = st.sidebar.multiselect(
    "Select Category ID",
    options=df["category_id"].unique(),
    default=df["category_id"].unique()
)

country = st.sidebar.multiselect(
    "Select Country",
    options=df["publish_country"].unique(),
    default=df["publish_country"].unique()
)

day = st.sidebar.multiselect(
    "Select Published Day",
    options=df["published_day_of_week"].unique(),
    default=df["published_day_of_week"].unique()
)

# Apply filters
filtered_df = df[
    (df["category_id"].isin(category)) &
    (df["publish_country"].isin(country)) &
    (df["published_day_of_week"].isin(day))
]

# ----------------------------
# Title
# ----------------------------
st.title("📊 YouTube Trending Videos Analytics")
st.markdown("Interactive dashboard to analyze trending YouTube videos")

# ----------------------------
# KPI Metrics
# ----------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "👀 Total Views",
    f"{filtered_df['views'].sum():,}"
)

col2.metric(
    "👍 Total Likes",
    f"{filtered_df['likes'].sum():,}"
)

col3.metric(
    "💬 Total Comments",
    f"{filtered_df['comment_count'].sum():,}"
)

st.divider()

# ----------------------------
# Charts Row 1
# ----------------------------
col4, col5 = st.columns(2)

# Views by Category
views_by_category = (
    filtered_df.groupby("category_id")["views"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    views_by_category,
    x="category_id",
    y="views",
    title="Total Views by Category",
    labels={"category_id": "Category ID", "views": "Views"},
    color="views"
)

col4.plotly_chart(fig1, use_container_width=True)

# Likes vs Views
fig2 = px.scatter(
    filtered_df,
    x="views",
    y="likes",
    title="Likes vs Views",
    labels={"views": "Views", "likes": "Likes"},
    opacity=0.6
)

col5.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# Charts Row 2
# ----------------------------
col6, col7 = st.columns(2)

# Comments by Day
comments_day = (
    filtered_df.groupby("published_day_of_week")["comment_count"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    comments_day,
    x="published_day_of_week",
    y="comment_count",
    title="Comments by Published Day",
    markers=True
)

col6.plotly_chart(fig3, use_container_width=True)

# Country-wise Views
country_views = (
    filtered_df.groupby("publish_country")["views"]
    .sum()
    .reset_index()
)

fig4 = px.pie(
    country_views,
    names="publish_country",
    values="views",
    title="Views Distribution by Country"
)

col7.plotly_chart(fig4, use_container_width=True)

# ----------------------------
# Top Videos Table
# ----------------------------
st.subheader("🔥 Top 10 Trending Videos by Views")

top_videos = filtered_df.sort_values(
    by="views",
    ascending=False
).head(10)

st.dataframe(
    top_videos[
        ["title", "channel_title", "views", "likes", "comment_count"]
    ],
    use_container_width=True
)

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.markdown(
    "📌 **Project:** YouTube Trending Videos Analysis  \n"
    "📊 **Built with Streamlit**"
)
