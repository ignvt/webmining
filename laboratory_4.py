from sklearn.neighbors import NearestNeighbors


def get_filtered_by_genres(films_list_viewed, films_list):
    filtered_by_genres = []
    for viewed in films_list_viewed:
        for film in films_list:
            if set(viewed["genres"]).intersection(film["genres"]) and viewed["name"] not in [item["name"] for item in
                                                                                             filtered_by_genres]:
                filtered_by_genres.append({"name": film["name"], "rating": film["rating"]})
    return filtered_by_genres


def recommendation(filtered_by_genres, indices):
    return [filtered_by_genres[index]["name"] for index in indices[0]]


def nearest_neighbors(filtered_by_genres, films_list_viewed):
    neighbors = NearestNeighbors(n_neighbors=3)
    neighbors.fit([[film["rating"]] for film in filtered_by_genres])
    distances, indices = neighbors.kneighbors(
        [[sum([item["rating"] for item in films_list_viewed]) / len([item["rating"] for item in films_list_viewed])]])
    return indices


def main():
    films_list = [
        {"name": "The Shawshank Redemption", "rating": 9.3, "genres": ["Drama", "Mystery", "Thriller"]},
        {"name": "The Godfather", "rating": 9.2, "genres": ["Drama", "Crime", "Thriller"]},
        {"name": "The Dark Knight", "rating": 9.0, "genres": ["Action", "Crime", "Drama"]},
        {"name": "12 Angry Men", "rating": 8.9, "genres": ["Drama", "Crime", "Thriller"]},
        {"name": "Schindler's List", "rating": 8.9, "genres": ["Biography", "Drama", "History"]},
        {"name": "The Lord of the Rings: The Return of the King", "rating": 8.9,
         "genres": ["Action", "Adventure", "Drama"]},
        {"name": "Pulp Fiction", "rating": 8.8, "genres": ["Crime", "Drama", "Thriller"]},
        {"name": "The Lord of the Rings: The Fellowship of the Ring", "rating": 8.8,
         "genres": ["Action", "Adventure", "Drama"]},
        {"name": "The Matrix", "rating": 8.7, "genres": ["Action", "Sci-Fi", "Thriller"]},
        {"name": "Fight Club", "rating": 8.7, "genres": ["Drama", "Crime", "Thriller"]},
        {"name": "The Silence of the Lambs", "rating": 8.6, "genres": ["Crime", "Drama", "Thriller"]},
        {"name": "The Usual Suspects", "rating": 8.6, "genres": ["Crime", "Drama", "Mystery"]},
        {"name": "Inception", "rating": 8.6, "genres": ["Action", "Adventure", "Sci-Fi"]},
        {"name": "The Matrix Reloaded", "rating": 8.5, "genres": ["Action", "Sci-Fi", "Thriller"]},
        {"name": "The Lord of the Rings: The Two Towers", "rating": 8.5, "genres": ["Action", "Adventure", "Drama"]},
        {"name": "Gladiator", "rating": 8.5, "genres": ["Action", "Drama", "Thriller"]},
        {"name": "The Dark Knight Rises", "rating": 8.4, "genres": ["Action", "Crime", "Drama"]},
        {"name": "The Lord of the Rings: The Three-Body Problem", "rating": 8.4,
         "genres": ["Action", "Adventure", "Drama"]},
        {"name": "The Departed", "rating": 8.3, "genres": ["Crime", "Drama", "Thriller"]},
        {"name": "The Amazing World of Gumball", "rating": 8.3, "genres": ["Animation", "Adventure", "Comedy"]},
        {"name": "The Lion King", "rating": 8.3, "genres": ["Animation", "Adventure", "Drama"]}
    ]

    films_list_viewed = [
        {"name": "Forrest Gump", "rating": 8.7, "genres": ["Drama", "Crime", "Thriller"]},
        {"name": "The Prestige", "rating": 8.4, "genres": ["Drama", "Mystery", "Thriller"]},
        {"name": "WALL-E", "rating": 8.3, "genres": ["Animation", "Adventure", "Comedy"]},
    ]

    filtered_by_genres = get_filtered_by_genres(films_list_viewed, films_list)
    indices = nearest_neighbors(filtered_by_genres, films_list_viewed)
    films = recommendation(filtered_by_genres, indices)
    print(films)


if __name__ == "__main__":
    main()
