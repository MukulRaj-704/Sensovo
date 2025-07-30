# %% [markdown]
# DATA CLEANING AND PREPROCESS
# 

# %% [markdown]
# IMPORTING LIBRARIES

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
# READING CSV FILES

# %%
movie= pd.read_csv('../data/tmdb_movie.csv')
print(movie.shape)
print(movie.isnull().sum())

# %% [markdown]
# EXTRACTING SELECTED COLUMNS

# %%
movies=movie[['id','title','genre_ids','overview','release_date']]
print(movies.shape)
print(movies.isnull().sum())
movies.head()

# %% [markdown]
# DELETING ROWS WITH NULL VALUES

# %%
movies.dropna(inplace=True)
print(movies.shape)

# %% [markdown]
# GENER ID TO GENERE NAME MAPPING FUNCTION

# %%
genre_id_to_name = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western"
}


# %% [markdown]
# IMPORTING ABSTRACT SYNTAX TREE(AST) TO CONVERT STRING OF LIST TO LIST 

# %% [markdown]
# STRING OF LIST COMPLEXITY

# %%
import ast
def genre_ids_to_names(genre_id_str):
    if isinstance(genre_id_str, str):
        genre_ids = ast.literal_eval(genre_id_str)
    else:  
        genre_ids = genre_id_str
    return [genre_id_to_name.get(gid, "Unknown") for gid in genre_ids]
movies['genres'] = movies['genre_ids'].apply(genre_ids_to_names)


# %%
movies['release_date'] = movies['release_date'].astype(str)
movies['release_year'] = movies['release_date'].str[:4].astype(int)

# %%
movies.drop(columns=['genre_ids', 'release_date'], inplace=True)
movies.head()

# %%
credit=pd.read_csv('../data/tmdb_credit.csv')
print(credit.shape)
print(credit.isnull().sum())

# %% [markdown]
# DROPING NULL VALUES

# %%
credit.dropna(inplace=True)
credit.isnull().sum()

# %% [markdown]
# RENAMING OF COLUMN TO MERGE BOTH CSV FILES

# %%
credit.rename(columns={'movie_id':'id'},inplace=True)

# %%
movie_credit = pd.merge(movies, credit, left_on='id', right_on='id')
movie_credit.head()

# %%
movie_credit.to_csv('movie_credit.csv', index=False)

# %% [markdown]
# DATA CLEANING FOR RATINGS

# %%
rating=pd.read_csv('../data/movielens_ratings.csv')
print(rating.shape)
print(rating.isnull().sum())

# %%
movielens=pd.read_csv('../data/movieslens.csv')
print(movielens.shape)
print(movielens.isnull().sum())

# %%
movie_rating=pd.merge(movielens,rating,left_on='movieId',right_on='movieId')
print(movie_rating.shape)
print(movie_rating.isnull().sum())
movie_rating.head()

# %% [markdown]
# SELECTING USER WHO GIVES A SPECIFIC NO OF RATTING

# %%
user_rating_count=movie_rating.groupby('userId')['rating'].count()
active_user=user_rating_count[user_rating_count>300].index
filtered_rating=movie_rating[movie_rating['userId'].isin(active_user)]


# %% [markdown]
# SELECTING BOOKS WITH MORE THAN A SPECIFIC NO OF RATING 

# %%
movie_rating_counts = filtered_rating.groupby('movieId')['rating'].count()
popular_movies = movie_rating_counts[movie_rating_counts > 300].index
final_ratings = filtered_rating[filtered_rating['movieId'].isin(popular_movies)]

# %%
final_ratings.to_csv('cleaned_rating.csv',index=False)


