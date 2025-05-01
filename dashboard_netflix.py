import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Set up the Streamlit page
st.set_page_config(
    page_title="Netflix Movies and TV Shows",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title heading
st.title("Netflix Data Analysis")

# Load the dataset
df = pd.read_csv('netflix_titles.csv')
df['date_added'] = pd.to_datetime(df['date_added'], format='mixed', errors='coerce')
df['year_added'] = df['date_added'].dt.year

# Filter data for movies and TV shows
movies = df[df['type'] == 'Movie'].copy()
tv_shows = df[df['type'] == 'TV Show'].copy()

# Sidebar for theme and filters
st.sidebar.title("Netflix Dashboard")
st.sidebar.markdown("---")

# Add theme selection to the sidebar
theme = st.sidebar.selectbox("Select Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""<style>.stApp {background-color: #1e1e1e; color: white;}</style>""", unsafe_allow_html=True)
elif theme == "Light":
    st.markdown("""<style>.stApp {background-color: white; color: black;}</style>""", unsafe_allow_html=True)

# Filters
st.sidebar.header("Filters")

# Filter based on Content Type (Movie or TV Show)
content_type_filter = st.sidebar.multiselect(
    'Select Content Type', 
    options=df['type'].unique(), 
    default=df['type'].unique().tolist()  # Default to all types
)

# Filter based on Year range
year_range = st.sidebar.slider(
    'Select Year Range', 
    min_value=int(df['year_added'].min()), 
    max_value=int(df['year_added'].max()), 
    value=(int(df['year_added'].min()), int(df['year_added'].max())), 
    step=1
)

# Apply the filters to the data
filtered_df = df[df['type'].isin(content_type_filter)]
filtered_df = filtered_df[(filtered_df['year_added'] >= year_range[0]) & (filtered_df['year_added'] <= year_range[1])]

# Tab bar for charts
tabs = st.tabs(["Overview", "Content Type Distribution", "Trends", "Genres", "Directors and Countries"])

# Overview tab
with tabs[0]:
    st.header("Overview of Netflix Data")
    st.write("Explore insights from Netflix's vast collection of movies and TV shows.")

# Content Type Distribution tab
with tabs[1]:
    st.header("Content Type Distribution")
    type_counts = filtered_df['type'].value_counts()
    fig = px.pie(
        names=type_counts.index, 
        values=type_counts.values, 
        title="Distribution of Content Types"
    )
    st.plotly_chart(fig)

# Trends tab
with tabs[2]:
    st.header("Trend of Movies and TV Shows Added Over Time")
    content_added_per_year = filtered_df.groupby(['year_added', 'type']).size().unstack(fill_value=0)
    fig = px.line(
        content_added_per_year.reset_index(),
        x='year_added',
        y=content_added_per_year.columns,
        labels={'year_added': 'Year', 'value': 'Number of Content Added'},
        title='Trend of Movies and TV Shows Added Over Time'
    )
    st.plotly_chart(fig)

# Genres tab
with tabs[3]:
    st.header("Top 10 Genres")
    genre_counts = filtered_df['listed_in'].str.split(', ', expand=True).stack().value_counts()
    top_genres = genre_counts.head(10)
    fig = px.bar(
        x=top_genres.index,
        y=top_genres.values,
        labels={'x': 'Genre', 'y': 'Number of Titles'},
        title='Top 10 Genres on Netflix',
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)

# Directors and Countries tab
with tabs[4]:
    col1, col2 = st.columns(2)

    # Top 10 Directors with Most Titles on Netflix
    with col1:
        st.subheader("Top 10 Directors with Most Titles on Netflix")
        plt.figure(figsize=(12, 6))
        sns.countplot(x='director', data=filtered_df, order=filtered_df['director'].value_counts().index[:10], palette='viridis')
        plt.title('Top 10 Directors with Most Titles on Netflix')
        plt.xlabel('Director')
        plt.ylabel('Number of Titles')
        plt.xticks(rotation=45)
        st.pyplot(plt)

    # Top 10 Countries with Most Titles on Netflix
    with col2:
        st.subheader("Top 10 Countries with Most Titles on Netflix")
        plt.figure(figsize=(12, 6))
        sns.countplot(x='country', data=filtered_df, order=filtered_df['country'].value_counts().index[:10], palette='viridis')
        plt.title('Top 10 Countries with Most Titles on Netflix')
        plt.xlabel('Country')
        plt.ylabel('Number of Titles')
        plt.xticks(rotation=45)
        st.pyplot(plt)
