import streamlit as st
import streamlit.components.v1 as components
from bookrec import get_book

st.set_page_config(page_title="Book Recommendations", layout="wide", page_icon="📚")
# Navigation Bar
col1, col2, col3 = st.columns([10, 1, 1.25])
with col3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("main.py")  

# Title
st.title(" Discover Books That Speak to You 📚")
src = st.columns(1)
with src[0]:
    book_input = st.text_input("Enter Book Nmae")

center_col = st.columns([1, 0.25, 1])[1]
with center_col:
    search = st.button("🔍 Recommend")

# Recommendation logic
if search:
    result = get_book(book_input)

    if not result.empty:
        st.markdown("### 🎯 Recommended Books:")
        result = result.head(30)
        html = """
        <style>
            .grid-container {
                display: grid;
                grid-template-columns: repeat(6, 1fr);
                gap: 20px;
                padding: 20px;
                background-color: #0e1117;
            }

            .book-card {
                text-align: center;
                background-color: #111;
                padding: 10px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
                transition: transform 0.2s;
            }

            .book-card:hover {
                transform: scale(1.05);
            }

            .book-image {
                width: 100%;
                height: 200px;
                object-fit: cover;
                border-radius: 6px;
            }

            .book-title {
                margin-top: 10px;
                font-weight: bold;
                color: white;
                font-size: 13px;
            }

            .book-author {
                font-size: 12px;
                color: #ccc;
                margin-top: 2px;
            }
        </style>
        <div class='grid-container'>
        """

        for _, row in result.iterrows():
            html += f"""
                <div class="book-card">
                    <img src="{row['Image-URL-L']}" class="book-image" alt="Cover" />
                    <div class="book-title">{row['Book-Title']}</div>
                    <div class="book-author">{row['Book-Author']}</div>
                </div>
            """

        html += "</div>"
        components.html(html, height=1800, scrolling=False)

    else:
        st.warning("❌ No matching book found or insufficient data for recommendations.")
