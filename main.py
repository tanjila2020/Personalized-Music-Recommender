from recommender import MusicRecommender

recommender = MusicRecommender(
    user_artists_path="user_artists.dat",
    artists_path="artists.dat"
)

recommendations = recommender.recommend_for_existing_user(user_id=2, top_n=10)

for rec in recommendations:
    print(rec)