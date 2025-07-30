import os
import re
import ast
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process, fuzz

# PATH SETUP 
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(os.path.dirname(current_dir), "data")
def make_poster_url(path):
    if pd.isna(path) or path.strip() == '' or path == 'No Image':
        return "https://via.placeholder.com/150x225?text=No+Image"
    return f"https://image.tmdb.org/t/p/w500{path}"

# LOAD DATA 
try:
    movie_credit = pd.read_csv(os.path.join(current_dir, "movie_credit.csv"))
    tmdb_movie = pd.read_csv(os.path.join(data_dir, "tmdb_movie.csv"))
except FileNotFoundError as e:
    print(f"Error loading data file: {e}. Please ensure all CSVs are in the 'data' folder.")
    raise

# CAST NAME EXTRACTION
def extract_and_format_names(cast_string):
    if pd.isna(cast_string) or cast_string.strip() == '':
        return ""
    cast_members = cast_string.split('\n')
    real_names = []
    for member in cast_members:
        match = re.match(r'([^ (]+(?: [^ (]+)*?)\s*\(', member)
        real_names.append(match.group(1).strip() if match else member.strip())
    return ' '.join(real_names)

movie_credit['real_names'] = movie_credit['top_5_cast'].apply(extract_and_format_names)
movie_credit.drop(columns=['top_5_cast'], inplace=True, errors='ignore')
movie_credit.drop_duplicates(subset='title', inplace=True)
movie_credit.fillna('', inplace=True)

# TEXT COMBINATION FOR CONTENT-BASED FILTERING 
def create_soup(row):
    genres_str = ''
    if isinstance(row['genres'], str):
        try:
            genres_list = ast.literal_eval(row['genres'])
            if isinstance(genres_list, list):
                genres_str = ' '.join(genres_list)
            else:
                genres_str = row['genres']
        except (ValueError, SyntaxError):
            genres_str = row['genres']
    elif isinstance(row['genres'], list):
        genres_str = ' '.join(row['genres'])
    else:
        genres_str = str(row['genres'])

    return ' '.join([
        str(row['title']),
        str(row['overview']),
        genres_str,
        str(row['director(s)']),
        str(row['real_names'])
    ])

movie_credit['soup'] = movie_credit.apply(create_soup, axis=1)

# TF-IDF VECTORIZER 
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movie_credit['soup'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
indices = pd.Series(movie_credit.index, index=movie_credit['title']).drop_duplicates()

# CONTENT-BASED RECOMMENDER 
def get_recommendations(title, cosine_sim=cosine_sim, num_recommendations=48):
    if title not in indices:
        fuzzy_match = process.extractOne(title, indices.index, scorer=fuzz.ratio)
        if fuzzy_match and fuzzy_match[1] > 80:
            title = fuzzy_match[0]
        else:
            return pd.DataFrame(columns=['title', 'poster_url', 'score'])

    idx = indices[title]
    sim_scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:num_recommendations-1]
    movie_indices = [i[0] for i in sim_scores]
    scores = [i[1] for i in sim_scores]

    recommended_movies_df = movie_credit.iloc[movie_indices].copy()
    recommended_movies_df['score'] = scores
    recommended_movies_df['poster_url'] = recommended_movies_df['poster_url'].apply(make_poster_url)

    return recommended_movies_df[['title', 'poster_url', 'score']].drop_duplicates(subset='title').head(num_recommendations)

# POPULARITY-BY-YEAR SETUP 
tmdb_movie['release_year'] = pd.to_datetime(tmdb_movie['release_date'], errors='coerce').dt.year

year_info = tmdb_movie[[
    'id', 'popularity', 'vote_count', 'vote_average',
    'release_date', 'poster_url', 'release_year'
]]

movie_year_df = pd.merge(
    year_info,
    movie_credit[['id', 'title']],
    on='id',
    how='inner'
)
movie_year_df.dropna(subset=['vote_average', 'vote_count'], inplace=True)
movie_year_df['vote_count'] = movie_year_df['vote_count'].astype(int)
c = movie_year_df['vote_average'].mean()
m = movie_year_df['vote_count'].quantile(0.53)

movie_year_df = movie_year_df[movie_year_df['vote_count'] >= m].copy()
if not movie_year_df.empty:
    movie_year_df['weighted_score'] = (
        (movie_year_df['vote_count'] / (movie_year_df['vote_count'] + m)) * movie_year_df['vote_average']
        + (m / (movie_year_df['vote_count'] + m)) * c
    )

# GET MOVIES BY YEAR
def get_movie_by_year(year, top_n=30):
    df_year = movie_year_df[movie_year_df['release_year'] == year].copy()

    if df_year.empty:
        return pd.DataFrame(columns=['title', 'poster_url', 'weighted_score'])

    df_year['poster_url'] = df_year['poster_url'].apply(make_poster_url)

    sort_col = 'weighted_score' if 'weighted_score' in df_year.columns else 'popularity'
    if sort_col == 'popularity':
        df_year['popularity'] = pd.to_numeric(df_year['popularity'], errors='coerce').fillna(0)

    return df_year.sort_values(by=sort_col, ascending=False)\
        .head(top_n)[['title', 'poster_url', sort_col]].rename(columns={sort_col: 'score'})
