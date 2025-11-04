import os
import requests

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


def search_movies(query):
    """Busca películas por texto"""
    url = f"{BASE_URL}/search/movie?api_key={TMDB_API_KEY}&language=es-ES&query={query}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    results = []
    for movie in data.get("results", []):
        poster_path = movie.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

        results.append({
            "tmdb_id": movie["id"],
            "title": movie.get("title", "Sin título"),
            "overview": movie.get("overview", ""),
            "poster_url": poster_url,
            "release_date": movie.get("release_date", ""),
            "rating": movie.get("vote_average", 0),
            "genre_ids": movie.get("genre_ids", []),
        })

    return results


def get_popular_movies(pages=5):
    """Trae múltiples páginas de películas populares"""
    results = []

    for page in range(1, pages + 1):
        url = f"{BASE_URL}/movie/popular?api_key={TMDB_API_KEY}&language=es-ES&page={page}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        for movie in data.get("results", []):
            poster_path = movie.get("poster_path")
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

            results.append({
                "tmdb_id": movie["id"],
                "title": movie.get("title", "Sin título"),
                "overview": movie.get("overview", ""),
                "poster_url": poster_url,
                "release_date": movie.get("release_date", ""),
                "rating": movie.get("vote_average", 0),
                "genre_ids": movie.get("genre_ids", []),
            })

    return results
