import streamlit as st
from utils.api import get_popular_movies, get_image_url

st.set_page_config(
    page_title="🎬 Mano-e-Pelis",
    page_icon="🎬",
    layout="wide"
)

if "favorites" not in st.session_state:
    st.session_state.favorites = {}

st.title("🎬 Mano-e-Pelis")
st.markdown("*Tu catálogo personal de películas*")
st.divider()

st.header("🔥 Películas Populares")

try:
    movies = get_popular_movies()
except Exception as e:
    st.error(f"❌ Error al cargar películas: {e}")
    st.stop()

cols = st.columns(4)

for i, movie in enumerate(movies[:12]):
    with cols[i % 4]:
        poster_url = get_image_url(movie.get("poster_path"))
        st.image(poster_url, use_container_width=True)
        st.markdown(f"**{movie['title']}**")
        rating = movie.get("vote_average", 0)
        st.caption(f"⭐ {rating:.1f}/10")
        overview = movie.get("overview", "Sin sinopsis disponible.")
        st.caption(overview[:100] + "..." if len(overview) > 100 else overview)

        movie_id = movie["id"]
        if movie_id in st.session_state.favorites:
            if st.button("💔 Quitar", key=f"rem_{movie_id}"):
                del st.session_state.favorites[movie_id]
                st.rerun()
        else:
            if st.button("❤️ Favorito", key=f"fav_{movie_id}"):
                st.session_state.favorites[movie_id] = {
                    "id": movie_id,
                    "title": movie["title"],
                    "poster_path": movie.get("poster_path"),
                    "vote_average": rating
                }
                st.rerun()
        st.divider()

st.markdown("---")
st.markdown("<div style='text-align:center;color:gray;'>Hecho con ❤️ y Python · Datos de <a href='https://www.themoviedb.org/'>TMDB</a></div>", unsafe_allow_html=True)
