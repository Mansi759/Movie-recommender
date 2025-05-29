import streamlit as st
import pickle
import pandas as pd
import requests
from streamlit_option_menu import option_menu
import gdown
import os

import os




# Constants
API_KEY = os.getenv("API_KEY")
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"
PLACEHOLDER_IMAGE = "https://via.placeholder.com/150"

# Load movies_dict.pkl
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))

# Download similarity.pkl if not already present
if not os.path.exists("similarity.pkl"):
    file_id = "1lyxJlR87ARHsaGfAzHRoVNRsVUnEHhB-"  # <-- Google Drive File ID
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    gdown.download(url, "similarity.pkl", quiet=False)

# Load similarity
similarity = pickle.load(open("similarity.pkl", "rb"))

# Create DataFrame
movies = pd.DataFrame(movies_dict)
movies["release_date"] = pd.to_datetime(movies["release_date"], errors="coerce")

# Fetch movie poster
def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}")
    data = response.json()
    return f"{POSTER_BASE_URL}{data.get('poster_path', '')}" if data.get("poster_path") else PLACEHOLDER_IMAGE

# Fetch movie details and cast
def fetch_movie_details(movie_id):
    movie_row = movies[movies["movie_id"] == movie_id].iloc[0]
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits")
    data = response.json()
    cast_list = data.get("credits", {}).get("cast", [])[:5]
    cast_names = [cast["name"] for cast in cast_list]
    cast_posters = [
        f"{POSTER_BASE_URL}{cast['profile_path']}" if cast.get("profile_path") else PLACEHOLDER_IMAGE
        for cast in cast_list
    ]
    return {
        "title": data.get("title", "Unknown Movie"),
        "overview": data.get("overview", "No overview available."),
        "rating": movie_row.get("vote_average", "N/A"),
        "popularity": movie_row.get("popularity", "N/A"),
        "release_year": data.get("release_date", "N/A")[:4] if data.get("release_date") else "N/A",
        "genre": ", ".join([genre['name'] for genre in data.get("genres", [])]),
        "poster": fetch_poster(movie_id),
        "cast_names": cast_names,
        "cast_posters": cast_posters
    }

# Recommend function
def recommend(movie):
    if movie not in movies["title"].values:
        return [], []
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    names = [movies.iloc[i[0]].title for i in movie_list]
    posters = [fetch_poster(movies.iloc[i[0]].movie_id) for i in movie_list]
    return names, posters

# Streamlit setup
st.set_page_config(page_title="🎬 Movie Recommender", page_icon="🎥", layout="wide")

# Sidebar
with st.sidebar:
    st.title("🎬 Movie Recommender")
    option = option_menu(
        "Menu",
        ["Home", "Trending Movies", "Top Rated Movies", "Latest Releases", "Blockbuster Movies"],
        icons=["house", "fire", "star", "clock", "cash"],
        default_index=0
    )

# Session state
if "selected_movie_id" not in st.session_state:
    st.session_state.selected_movie_id = None
if "selected_movie_name" not in st.session_state:
    st.session_state.selected_movie_name = None
if "show_more" not in st.session_state:
    st.session_state.show_more = False

# Movie Details Page
if st.session_state.selected_movie_id:
    movie_details = fetch_movie_details(st.session_state.selected_movie_id)
    st.header(f"🎬 {movie_details['title']}")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(movie_details['poster'], width=250)
    with col2:
        st.subheader("Overview")
        st.write(movie_details['overview'])
        st.write(f"⭐ Rating: {movie_details['rating']}")
        st.write(f"🔥 Popularity: {movie_details['popularity']}")
        st.write(f"📅 Release Year: {movie_details['release_year']}")
        st.write(f"🎭 Genre: {movie_details['genre']}")

    st.subheader("🎭 Top 5 Cast Members")
    cast_cols = st.columns(5)
    for col, name, poster in zip(cast_cols, movie_details["cast_names"], movie_details["cast_posters"]):
        with col:
            st.image(poster, width=100)
            st.caption(name)

    st.subheader("🎬 Recommended Movies")
    names, posters = recommend(movie_details["title"])
    if names:
        cols = st.columns(5)
        for col, name, poster in zip(cols, names, posters):
            with col:
                if st.button(name, key=f"recommend_{name}"):
                    st.session_state.selected_movie_id = movies[movies["title"] == name]["movie_id"].values[0]
                    st.rerun()
                st.image(poster, width=150)

    if st.button("🔙 Go Back to Home", key="go_back"):
        st.session_state.selected_movie_id = None
        st.rerun()

# Home Page
elif option == "Home":
    st.header("🔍 Movie Recommendation System")
    selected_movie_name = st.selectbox("Search for a movie", movies["title"].values, key="movie_search")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Recommend", key="recommend_button"):
            st.session_state.selected_movie_name = selected_movie_name
    with col2:
        if st.button("View Details", key="view_details_button"):
            st.session_state.selected_movie_id = movies[movies["title"] == selected_movie_name]["movie_id"].values[0]
            st.rerun()

    if st.session_state.selected_movie_name:
        st.subheader(f"🎬 Recommended Movies for {st.session_state.selected_movie_name}")
        names, posters = recommend(st.session_state.selected_movie_name)
        if names:
            cols = st.columns(5)
            for col, name, poster in zip(cols, names, posters):
                with col:
                    if st.button(name, key=f"recommend_{name}"):
                        st.session_state.selected_movie_id = movies[movies["title"] == name]["movie_id"].values[0]
                        st.rerun()
                    st.image(poster, width=150)

# Other Sections
else:
    section_titles = {
        "Trending Movies": "🔥 Trending Movies",
        "Top Rated Movies": "⭐ Top Rated Movies",
        "Latest Releases": "⏳ Latest Releases",
        "Blockbuster Movies": "💰 Blockbuster Movies"
    }
    st.header(section_titles.get(option, "🔥 Trending Movies"))

    sort_column = {
        "Trending Movies": "popularity",
        "Top Rated Movies": "vote_average",
        "Latest Releases": "release_date",
        "Blockbuster Movies": "revenue"
    }[option]

    filtered_movies = movies.sort_values(by=sort_column, ascending=False).head(10 if st.session_state.show_more else 5)

    cols = st.columns(5)
    for idx, (_, row) in enumerate(filtered_movies.iterrows()):
        with cols[idx % 5]:
            if st.button(row['title'], key=f"movie_{row['title']}"):
                st.session_state.selected_movie_id = row["movie_id"]
                st.rerun()
            st.image(fetch_poster(row["movie_id"]), width=150)

            detail = {
                "Trending Movies": f"🔥 Popularity: {row['popularity']}",
                "Top Rated Movies": f"⭐ Rating: {row['vote_average']}",
                "Latest Releases": f"📅 Release Year: {row['release_date'].year if pd.notna(row['release_date']) else 'N/A'}",
                "Blockbuster Movies": f"💰 Revenue: ${row['revenue']:,.0f}"
            }[option]
            st.caption(detail)

    if st.button("🔽 Show More" if not st.session_state.show_more else "🔼 Show Less"):
        st.session_state.show_more = not st.session_state.show_more
        st.rerun()





