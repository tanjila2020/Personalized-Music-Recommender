import streamlit as st
from recommender import MusicRecommender

# Load recommender
@st.cache_resource
def load_model():
    return MusicRecommender(
        user_artists_path="user_artists.dat",
        artists_path="artists.dat"
    )

recommender = load_model()

st.title("🎧 Personalized Music Recommender")

mode = st.radio(
    "Choose recommendation type:",
    ["Existing User", "New User"]
)

# -------------------------------
# EXISTING USER MODE
# -------------------------------
if mode == "Existing User":
    st.subheader("🔍 Recommend for Existing User")

    user_id = st.number_input("Enter User ID:", min_value=1, step=1)

    top_n = st.slider("Number of recommendations:", 5, 20, 10)

    if st.button("Recommend for User"):
        results = recommender.recommend_for_existing_user(user_id, top_n)

        if not results:
            st.warning("User not found or no recommendations available.")
        else:
            st.subheader("Recommended Artists")

            for r in results:
                st.write(f"🎵 {r['artist_name']} (Score: {r['score']})")


# -------------------------------
# NEW USER MODE
# -------------------------------
else:
    st.subheader("✨ Recommend for New User")

    # Load artist list
    artist_df = recommender.artists

    artist_options = artist_df["name"].sort_values().tolist()

    selected_artists = st.multiselect(
        "Select 3–5 artists you like:",
        artist_options
    )

    top_n = st.slider("Number of recommendations:", 5, 20, 10)

    if st.button("Get Recommendations"):
        if len(selected_artists) < 3:
            st.warning("Please select at least 3 artists.")
        else:
            # Convert names to IDs
            artist_ids = artist_df[
                artist_df["name"].isin(selected_artists)
            ]["id"].tolist()

            results = recommender.recommend_for_new_user(artist_ids, top_n)

            if not results:
                st.warning("No recommendations found.")
            else:
                st.subheader("Recommended Artists")

                for r in results:
                    st.write(f"🎵 {r['artist_name']} (Score: {r['score']})")