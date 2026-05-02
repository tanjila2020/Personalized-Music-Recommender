import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class MusicRecommender:
    def __init__(self, user_artists_path, artists_path):
        self.user_artists = pd.read_csv(user_artists_path, sep="\t")
        self.artists = pd.read_csv(artists_path, sep="\t")

        self.user_artist_matrix = self.user_artists.pivot_table(
            index="userID",
            columns="artistID",
            values="weight",
            fill_value=0
        )

        self.user_similarity = cosine_similarity(self.user_artist_matrix)

        self.user_similarity_df = pd.DataFrame(
            self.user_similarity,
            index=self.user_artist_matrix.index,
            columns=self.user_artist_matrix.index
        )

    def recommend_for_existing_user(self, user_id, top_n=10):
        if user_id not in self.user_artist_matrix.index:
            return []

        similar_users = (
            self.user_similarity_df[user_id]
            .sort_values(ascending=False)
            .drop(user_id)
            .head(5)
            .index
        )

        user_listened = self.user_artist_matrix.loc[user_id]
        user_listened_artists = set(user_listened[user_listened > 0].index)

        similar_user_data = self.user_artist_matrix.loc[similar_users]
        artist_scores = similar_user_data.sum(axis=0)

        recommendations = artist_scores.drop(
            labels=user_listened_artists,
            errors="ignore"
        )

        recommendations = recommendations.sort_values(ascending=False).head(top_n)

        return self._format_recommendations(recommendations)

    def recommend_for_new_user(self, liked_artist_ids, top_n=10):
        temp_user = pd.Series(
            0,
            index=self.user_artist_matrix.columns
        )

        for artist_id in liked_artist_ids:
            if artist_id in temp_user.index:
                temp_user[artist_id] = 100

        temp_similarity = cosine_similarity(
            [temp_user],
            self.user_artist_matrix
        )[0]

        similar_users = pd.Series(
            temp_similarity,
            index=self.user_artist_matrix.index
        ).sort_values(ascending=False).head(5).index

        similar_user_data = self.user_artist_matrix.loc[similar_users]
        artist_scores = similar_user_data.sum(axis=0)

        recommendations = artist_scores.drop(
            labels=liked_artist_ids,
            errors="ignore"
        )

        recommendations = recommendations.sort_values(ascending=False).head(top_n)

        return self._format_recommendations(recommendations)

    def _format_recommendations(self, recommendations):
        results = []

        if recommendations.empty:
            return results

        max_score = recommendations.max()

        for artist_id, score in recommendations.items():
            artist_name = self.artists.loc[
                self.artists["id"] == artist_id,
                "name"
            ].values

            if len(artist_name) > 0:
                normalized_score = score / max_score if max_score > 0 else 0

                results.append({
                    "artist_id": artist_id,
                    "artist_name": artist_name[0],
                    "score": round(normalized_score, 3)
                })

        return results