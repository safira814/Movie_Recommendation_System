import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=19c3b1068e33282ddb03002cfe5356cb&language=en-US".format(
            movie_id
        )
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]


# Function to recommend similar movies
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
        1:6
    ]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# Load data
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# Set page title and favicon
st.set_page_config(page_title="Movie Recommender", page_icon=":movie_camera:")


# Main title
st.title("Movie Recommender System")

# Dropdown to select a movie
selected_movie_name = st.selectbox("Search for a movie", movies["title"].values)

# Button to trigger recommendation
if st.button("Get Recommendations"):
    names, posters = recommend(selected_movie_name)

    # Calculate number of columns based on number of recommendations
    num_cols = min(5, len(posters))

    # Display recommended movies and posters in a grid layout
    cols = st.columns(num_cols)  # Create columns

    for i in range(num_cols):
        with cols[i]:
            st.subheader(names[i])
            st.image(posters[i], use_column_width=True)
