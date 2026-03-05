import streamlit as st
from utils.api import get_image_url

st.set_page_config(page_title="Favoritos - Mano-e-Pelis", page_icon="❤️", layout="wide")

if "favorites" not in st.session_state:
    st.session_state.favorites = {}

st.title("❤️ Mis Películas Favoritas")

favorites = st.session_state.favorites

if not favorites:
    st.info("🎬 Aún no tienes películas favoritas.")
    st.markdown("Ve a **App** o **Buscar** para agregar películas a tu lista.")
else:
    st.success(f"Tienes **{len(favorites)}** película(s) en tu lista.")

    if st.button("🗑️ Borrar todos los favoritos"):
        st.session_state.favorites = {}
        st.rerun()

    st.divider()

    cols = st.columns(4)

    for i, (movie_id, movie) in enumerate(favorites.items()):
        with cols[i % 4]:
            st.image(get_image_url(movie.get("poster_path")), use_container_width=True)
            st.markdown(f"**{movie['title']}**")
            st.caption(f"⭐ {movie.get('vote_average', 0):.1f}/10")

            if st.button("💔 Quitar", key=f"favpage_rem_{movie_id}"):
                del st.session_state.favorites[movie_id]
                st.rerun()

            st.divider()