import os
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Get absolute path to the directory where bookrec.py lives
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one level to reach Sensovo/ and then into the data folder
data_path = os.path.join(current_dir, "..", "data")
book = pd.read_csv(os.path.join(data_path, "book.csv"))  # Contains ISBN, Book-Title, Image-URL-L, etc.
rating = pd.read_csv(os.path.join(data_path, "book_rating.csv"))
user = pd.read_csv(os.path.join(data_path, "book_user.csv"))

book.dropna(inplace=True)
rating_name = rating.merge(book, on="ISBN")

# Filter active users
active_users = rating_name.groupby('User-ID').count()['Book-Rating'] > 200
active_users = active_users[active_users].index
filtered_user = rating_name[rating_name['User-ID'].isin(active_users)]

# Filter popular books
popular_books = filtered_user.groupby('Book-Title').count()['Book-Rating'] > 50
popular_books = popular_books[popular_books].index
filtered_books = filtered_user[filtered_user['Book-Title'].isin(popular_books)]

# Create pivot table (Book-Title vs User-ID matrix)
pt = filtered_books.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating').fillna(0)

# Cosine similarity
similarity_score = cosine_similarity(pt)

# Recommendation function
def get_book(name, top_n=30):
    try:
        index = np.where(pt.index == name)[0][0]
    except IndexError:
        return pd.DataFrame(columns=['Book-Title', 'Image-URL-L', 'Book-Author'])

    distances = similarity_score[index]
    similarity_items = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:top_n+1]
    recommended_titles = [pt.index[i[0]] for i in similarity_items]

    # Get titles, author and poster URLs
    book_info = (
        book[book['Book-Title'].isin(recommended_titles)]
        .drop_duplicates(subset='Book-Title')[
            ['Book-Title', 'Image-URL-L', 'Book-Author']  # include author here
        ]
    )

    return book_info

