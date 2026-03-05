import streamlit as st
from utils.api import search_movies, get_movie_details, get_image_url

st.set_page_config(page_title="Buscar - Mano-e-Pelis", page_icon="🔍", layout="wide")

if "favorites" not in st.session_state:
    st.session_state.favorites = {}

st.title("🔍 Buscar Películas")

query = st.text_input(
    "¿Qué película estás buscando?",
    placeholder="Escribe el nombre de una película..."
)

if query:
    with st.spinner("Buscando..."):
        try:
            results = search_movies(query)
        except Exception as e:
            st.error(f"❌ Error en la búsqueda: {e}")
            st.stop()

    if not results:
        st.warning("😕 No se encontraron películas con ese nombre.")
    else:
        st.success(f"🎬 {len(results)} resultados encontrados")

        for movie in results[:10]:
            col_img, col_info = st.columns([1, 3])

            with col_img:
                st.image(get_image_url(movie.get("poster_path")), use_container_width=True)

            with col_info:
                st.subheader(movie["title"])
                release = movie.get("release_date", "Desconocido")
                rating = movie.get("vote_average", 0)
                st.markdown(f"📅 **{release}** · ⭐ **{rating:.1f}**/10")
                st.write(movie.get("overview", "Sin sinopsis disponible."))

                movie_id = movie["id"]
                if movie_id in st.session_state.favorites:
                    if st.button("💔 Quitar de favoritos", key=f"search_rem_{movie_id}"):
                        del st.session_state.favorites[movie_id]
                        st.rerun()
                else:
                    if st.button("❤️ Agregar a favoritos", key=f"search_fav_{movie_id}"):
                        st.session_state.favorites[movie_id] = {
                            "id": movie_id,
                            "title": movie["title"],
                            "poster_path": movie.get("poster_path"),
                            "vote_average": rating
                        }
                        st.rerun
