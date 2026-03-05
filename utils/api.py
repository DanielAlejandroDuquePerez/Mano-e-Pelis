import streamlit as st
import requests

API_KEY = st.secrets["tmdb_api_key"]
BASE_URL = "https://api.themoviedb.org/3"
IMG_BASE_URL = "https://image.tmdb.org/t/p/w500"
PLACEHOLDER_IMG = "https://via.placeholder.com/500x750?text=Sin+Imagen"


@st.cache_data(ttl=600)
def get_popular_movies(page=1):
    url = f"{BASE_URL}/movie/popular"
    params = {"api_key": API_KEY, "language": "es-ES", "page": page}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()["results"]


@st.cache_data(ttl=600)
def search_movies(query, page=1):
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "language": "es-ES", "query": query, "page": page}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()["results"]


@st.cache_data(ttl=600)
def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY, "language": "es-ES"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_image_url(poster_path):
    if poster_path:
        return f"{IMG_BASE_URL}{poster_path}"
    return PLACEHOLDER_IMG
