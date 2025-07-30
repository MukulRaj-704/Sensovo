# app/main.py

import streamlit as st

st.set_page_config(page_title="Home - Sensovo", layout="wide", page_icon="🏡") # Added page_icon for consistency
st.title("What to Watch or Read Next? Sensovo Knows!")
st.write('Sensovo is your smart companion for discovering movies and books tailored to your taste.')
st.markdown("---") # Add a separator for better visual appeal

st.write("Select what you want!")

col1, col2 = st.columns(2)

with col1:
    if st.button("Discover Movies You'll Love 🎬", use_container_width=True): # Added emojis and use_container_width
        st.switch_page("pages/movie.py") # This will switch to app/pages/movie.py

with col2:
    if st.button("Let the Right Book Find You 📖", use_container_width=True): # Added emojis and use_container_width
        st.switch_page("pages/book.py") # This will switch to app/pages/book.py
        st.write(' ')
st.markdown("---")

st.markdown("""
<div style='font-size:18px;'>
🎬📚 <strong>Sensovo</strong> is your personalized media companion — helping you explore the world of movies and books with ease and excitement.<br><br>
🔍 Whether you're in the mood for a classic film or a hidden literary gem, Sensovo lets you search by <strong>movie name, release year, or book title</strong> to match your unique interests.<br><br>
🤖 Powered by smart recommendation algorithms, it curates suggestions that suit your taste — so you're never stuck wondering what to watch or read next.<br><br>
🚀 From late-night binge-worthy films to inspiring page-turners, Sensovo brings entertainment discovery to your fingertips — all in one place!
</div>
""", unsafe_allow_html=True)
