import streamlit as st
import requests

# =============================
# CONFIG
# =============================
API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# =============================
# TITLE
# =============================
st.title("🎬 Movie Recommendation System")

st.markdown("Type a movie name and get recommendations with posters")

# =============================
# INPUT
# =============================
movie_name = st.text_input("Enter Movie Name")

# =============================
# BUTTON
# =============================
if st.button("Recommend"):

    if not movie_name:
        st.warning("Please enter a movie name")
    else:
        try:
            url = f"{API_BASE}/recommend?title={movie_name}"
            response = requests.get(url)
            data = response.json()

            if not data:
                st.error("No recommendations found")
            else:
                st.subheader("Recommended Movies")

                cols = st.columns(5)

                for i, movie in enumerate(data):
                    with cols[i % 5]:
                        if movie.get("poster") and movie["poster"] != "N/A":
                            st.image(movie["poster"])
                        else:
                            st.write("No Image")

                        st.write(movie["title"])
                        st.caption(f"⭐ {movie.get('rating', 'N/A')}")

        except Exception as e:
            st.error(f"Error: {e}")