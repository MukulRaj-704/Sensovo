import streamlit as st
import pandas as pd

st.set_page_config(page_title="📊 Data Overview", layout="wide")

# === HEADER ===
st.title("📊 Data Overview")
st.markdown("""
Welcome to the **Sensovo** Data Overview page.  
Ever wondered what's under the hood of a great recommendation? Our "Data Overview" page pulls back the curtain! For movies, we've blended the rich details of TMDB (think plot, cast, and those awesome posters!) with the genuine user opinions from MovieLens. And for our book lovers? A fantastic Kaggle dataset provides all the ingredients for your next page-turner. We've meticulously cleaned, transformed, and shaped every bit of this data, making sure our system learns from the best, so you always get the perfect suggestion. Dive in to see the data magic!
""")
# === MOVIE SECTION ===
st.header("🎬 Movie Recommendation System")

with st.expander("✅ Datasets Used"):
    st.markdown("""
    - **TMDB API**
        - Accessed using personal API key
        - Fetched metadata like: Title, Genres, Overview, Cast, Crew, Keywords, Popularity, Ratings
        
    - **MovieLens 20M Dataset**
        - Source: [https://grouplens.org/datasets/movielens/](https://grouplens.org/datasets/movielens/)
        - Files Used:
            - `movies.csv`: Movie IDs and titles
            - `ratings.csv`: User ratings
            - `links.csv`: Mapping between MovieLens and TMDB/IMDB IDs
    """)

with st.expander("📁 Features Extracted and Used"):
    st.markdown("""
    - From **TMDB**:
        - `title`, `overview`, `genres`, `release_year`, `popularity`, `vote_average`,`vote_count`
        - Extracted top 3 cast members, director, and keywords
    - From **MovieLens**:
        - `userId`, `movieId`, `rating`
    """)



# === BOOK SECTION ===
st.header("📚 Book Recommendation System")

with st.expander("✅ Dataset Used"):
    st.markdown("""
    - **Book-Crossing Dataset** (Kaggle)
        - Source: [https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)
        - Files Used:
            - `Books.csv`: Title, Author, Publisher, ISBN, Year
            - `Ratings.csv`: User ratings for books
            - `Users.csv`: Location and age
    """)

with st.expander("📁 Features Used"):
    st.markdown("""
    - `bookTitle`, `bookAuthor`, `yearOfPublication`, `publisher`
    - `userId`, `bookRating`
    - `location`, `age`
    """)

with st.expander("🛠️ Preprocessing Steps"):
    st.markdown("""
    - Cleaned invalid or zero ratings
    - Removed duplicate book titles
    - Normalized case for titles/authors
    - Optionally filtered users with fewer than X ratings
    """)

# === DATA SIZE SUMMARY TABLE ===
st.header("📐 Dataset Summary")

summary_data = {
    "Dataset": ["TMDB (API)", "MovieLens M", "Kaggle Books"],
    "Records (approx)": ["~10,000", "~20,000,000", "~270,000"],
    "Used For": [
        "Content-Based Filtering (metadata, cast, etc.)",
        "Collaborative Filtering (user ratings)",
        "Book Recommendation (ratings + metadata)"
    ]
}
summary_df = pd.DataFrame(summary_data)
st.table(summary_df)
st.markdown("""
---
🔍 **Note**: All datasets are used for educational purposes and follow their respective usage licenses.  
🔍 **Note**:TMDB data was retrieved using a registered API key via their developer portal.
""")
