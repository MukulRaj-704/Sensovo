import streamlit as st
import pandas as pd
# Import get_recommendations from movierec
from movierec import  get_movie_by_year, get_recommendations

st.set_page_config(page_title="Movie Recommender", layout="wide", page_icon="🎬")

# Top navigation
col1, col2, col3 = st.columns([10, 1, 1.25])
with col3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("main.py")

st.title("Discover Movies You'll Love 🎬")

# Input fields
col1, col2 = st.columns(2)
with col1:
    movie_input = st.text_input("🎥 Enter Movie Name")
with col2:
    year_input = st.text_input("📅 Enter Release Year")

st.markdown("---")

# Recommend button centered
center_col = st.columns([1, 0.25, 1])[1]
with center_col:
    recommend_clicked = st.button("🔍 Recommend")

# Logic when button is clicked
if recommend_clicked:
    if movie_input and year_input:
        st.warning("⚠️ Please fill only one field: Movie or Year — not both.")
    elif not movie_input and not year_input:
        st.warning("⚠️ Please enter a movie name or year.")
    
    elif movie_input:
        try:
            st.subheader("🎬 Recommended Movies")
            results = get_recommendations(movie_input, num_recommendations=50) # Pass num_recommendations here if you want to control it from Streamlit

            if results.empty:
                st.info("💡 No recommendations found for this movie. Please try another one or check your data/filtering.")
            else:
                cols_per_row = 6
                for i in range(0, len(results), cols_per_row):
                    cols_list = st.columns(cols_per_row)
                    for idx, movie in enumerate(results.iloc[i:i+cols_per_row].itertuples(), start=0):
                        with cols_list[idx]:
                            st.image(movie.poster_url, width=150)
                            st.markdown(f"**{movie.title}**")
                            
        except Exception as e:
            st.error(f"❌ An error occurred while fetching recommendations: {e}")
            st.exception(e) 

    elif year_input:
        try:
            year = int(year_input)
            st.subheader(f"📅 Top Movies from {year}:")
            results = get_movie_by_year(year) 

            if results.empty:
                st.info("💡 No data available for this year.")
            else:
                cols_per_row = 6
                for i in range(0, len(results), cols_per_row):
                    cols_list = st.columns(cols_per_row)
                    for idx, movie in enumerate(results.iloc[i:i+cols_per_row].itertuples(), start=0):
                        with cols_list[idx]:
                            st.image(movie.poster_url, width=150)
                            st.markdown(f"**{movie.title}**")
                            
        except ValueError:
            st.error("Please enter a valid year (e.g., 2015).")
        except Exception as e:
            st.error(f"❌ An error occurred while fetching movies by year: {e}")
            st.exception(e) 