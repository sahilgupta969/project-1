import streamlit as st
import pickle
import pandas as pd
import requests
import time
from requests.exceptions import RequestException

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=dbf1bef642d7967257529f2f64b760ea&language=en-US'
    for _ in range(3):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        except RequestException as e:
            st.error(f"Error fetching poster: {e}")
            time.sleep(2)  # Wait before retrying
    return "https://via.placeholder.com/500x750?text=No+Image+Available"



def Recommend(movie):
    movie_index = movies[movies['title'] == movie ].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x : x[1])[1:21]
    recommended_movies = []
    recommend_movies_posters = []
    for j in movie_list:
        movie_id = movies.iloc[j[0]].movie_id
        recommended_movies.append(movies.iloc[j[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommend_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

css1 = """
    <style>
        .stApp {
            background-color: #000000; /* Black color */
        }
        .stButton button {
            background-color: #ff5733;
            color: #ffffff;
            border: none;
        }
        .stButton button:hover {
            background-color: #c70039; /* Hover color */
        }
    </style>
"""

# Inject custom CSS into the Streamlit app
st.markdown(css1, unsafe_allow_html=True)
st.title('Homogeneous Movie Recommender ')

search_query = st.text_input('Search for a movie:')
if st.button('Submission'):
    if search_query:
        filtered_movies = movies[movies['title'].str.contains(search_query, case=False)]
        if not filtered_movies.empty:
            selected_movie = filtered_movies.iloc[0]['title']  # Automatically select the first matching movie
            names, posters = Recommend(selected_movie)

            # Create columns for displaying posters horizontally
            cols = st.columns(5)  # Creates a 5-column layout

            for i in range(0, 20, 5):
                with st.container():
                    row_cols = st.columns(5)
                    for j in range(5):
                        idx = i + j
                        if idx < len(names):
                            with row_cols[j]:
                                st.text(names[idx])
                                st.image(posters[idx])
        else:
            st.error('No movies found with that name.')
    else:
        st.warning('Please enter a movie name to search.')
