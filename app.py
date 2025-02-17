import streamlit as st
import pickle
import requests
import os

# Function to fetch movie details from TMDB API
def fetch_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    response = requests.get(url)
    data = response.json()
    details = {
        "poster": f"https://image.tmdb.org/t/p/w500/{data.get('poster_path', '')}",
        "title": data.get('title', 'N/A'),
        "overview": data.get('overview', 'No overview available.'),
        "release_date": data.get('release_date', 'N/A'),
        "rating": data.get('vote_average', 'N/A'),
        "genres": ", ".join([genre['name'] for genre in data.get('genres', [])])
    }
    return details

# Function to reconstruct similarity.pkl from smaller parts
def reconstruct_similarity():
    PARTS_DIR = "similarity_parts"
    
    if not os.path.exists(PARTS_DIR):
        raise FileNotFoundError("❌ Error: similarity_parts directory not found!")

    part_files = sorted([f for f in os.listdir(PARTS_DIR) if f.startswith("similarity_part_")])
    
    if not part_files:
        raise FileNotFoundError("❌ Error: No similarity matrix parts found!")

    data = bytearray()  # Use bytearray to properly concatenate binary data
    for part in part_files:
        part_path = os.path.join(PARTS_DIR, part)
        with open(part_path, "rb") as f:
            data.extend(f.read())

    # Deserialize the reconstructed similarity matrix
    try:
        similarity_matrix = pickle.loads(data)
        return similarity_matrix
    except pickle.UnpicklingError:
        raise ValueError("❌ Error: Failed to reconstruct similarity matrix. Ensure all parts are present and not corrupted.")

# Load movie data
movies = pickle.load(open("movies_list.pkl", 'rb'))

# Reconstruct similarity matrix if parts exist
if os.path.exists("similarity_parts"):
    st.info("🔄 Reconstructing similarity matrix...")
    similarity = reconstruct_similarity()
else:
    st.error("❌ Error: Similarity matrix parts not found!")
    similarity = None

movies_list = movies['title'].values

# Streamlit UI
st.title("🎬 Movie Recommender System")

# Select a movie from dropdown
selectvalue = st.selectbox("🔍 Select a movie:", movies_list)

# Fetch selected movie details
selected_movie_id = movies[movies['title'] == selectvalue].iloc[0].id
selected_movie_details = fetch_details(selected_movie_id)

# Display the selected movie's poster (smaller size)
if selected_movie_details['poster']:
    st.image(selected_movie_details['poster'], width=200, caption=selected_movie_details['title'])

# Recommendation function
def recommend(movie):
    if similarity is None:
        st.error("❌ Similarity matrix not loaded. Cannot generate recommendations.")
        return []

    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie_ids = [movies.iloc[i[0]].id for i in distance[1:6]]
    return recommend_movie_ids

# Show recommended movies
if st.button("🎥 Show Recommendations"):
    if similarity is None:
        st.error("❌ Cannot generate recommendations because similarity matrix is missing.")
    else:
        st.subheader("🔥 Recommended Movies:")
        movie_ids = recommend(selectvalue)
        cols = st.columns(5)
        for idx, movie_id in enumerate(movie_ids):
            details = fetch_details(movie_id)
            with cols[idx]:
                st.image(details['poster'], use_container_width=True, caption=details['title'])
                st.write(f"**📅 Release Date:** {details['release_date']}")
                st.write(f"**⭐ Rating:** {details['rating']}")
                st.write(f"**🎭 Genres:** {details['genres']}")
                st.write(f"**📖 Overview:** {details['overview']}\n")
