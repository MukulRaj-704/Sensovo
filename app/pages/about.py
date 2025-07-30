import streamlit as st

st.set_page_config(page_title="📚🎬 Sensovo Overview", layout="wide")

# === PROJECT INTRODUCTION ===
st.title(" Welcome to Sensovo")
st.markdown("""
**Sensovo** is your intelligent media companion — designed to help you discover personalized movie and book recommendations effortlessly.

Whether you're in the mood for an epic film or a compelling read, Sensovo offers smart, dynamic suggestions tailored to your unique interests.

---

### 🔍 What Does Sensovo Offer?

#### 🎥 **Movie Recommendation Features**
- **Content-Based Filtering**  
  Suggests similar movies using genres, overviews, cast, crew, and keywords (powered by TMDB).
  
- **Collaborative Filtering**  
  Learns from user ratings and behaviors using the MovieLens M dataset to recommend movies you might enjoy.
  
- **Hybrid Model**  
  Combines metadata and user preferences for more accurate, personalized movie recommendations.

#### 📖 **Book Recommendation Features**
- **Content + Ratings Based Suggestion**  
  Based on the Book-Crossing dataset, Sensovo offers personalized book recommendations using both reader ratings and book metadata.
  
- **User Demographic Filtering (Optional)**  
  Location and age filters help tailor recommendations for specific audiences.

""")
