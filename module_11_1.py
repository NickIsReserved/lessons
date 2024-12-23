import json
from typing import List
import pandas as pd
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


class Movie:
    def __init__(self, name: str, rating: float, year: int, actors: List[str],
                 directors: List[str], desc: str, genre: List[str],
                 imdb_url: str):
        self.name = name
        self.rating = rating
        self.year = year
        self.actors = actors
        self.directors = directors
        self.desc = desc
        self.genre = genre
        self.imdb_url = imdb_url

    def __repr__(self):
        return f"Movie(name={self.name}, year={self.year}, rating={self.rating})"


def load_movies(filename: str) -> List[Movie]:
    """Функция загрузки JSON и создания списка Movie"""
    movies = []
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            movie = Movie(
                name=item['name'],
                rating=float(item['rating']),
                year=int(item['year']),
                actors=item['actors'],
                directors=item['directors'],
                desc=item['desc'],
                genre=item['genre'],
                imdb_url=item['imdb_url']
            )
            movies.append(movie)
    return movies


movies_list = load_movies('top250_min.json')

# Топ 10 фильмов с наибольшим рейтингом
top_rated_movies = sorted(movies_list, key=lambda x: x.rating, reverse=True)[
                   :10]

print("Топ 10 фильмов с наибольшим рейтингом:")
for i, movie in enumerate(top_rated_movies, 1):
    print(f"{i}. {movie.name} ({movie.year}) - Рейтинг: {movie.rating}")

# Топ 10 популярных актёров
all_actors = [actor for movie in movies_list for actor in movie.actors]

actor_counts = Counter(all_actors)
top_actors = actor_counts.most_common(10)  # Top 10 actors

print('\nТоп 10 популярных актёров:')
for actor, count in top_actors:
    print(f"{actor}: {count} фильмов")

# Использование библиотеки pandas
genres_by_year = []
for movie in movies_list:
    for genre in movie.genre:
        genres_by_year.append((genre, movie.year))

df = pd.DataFrame(genres_by_year, columns=['Genre', 'Year'])

genre_year_counts = df.groupby(['Year', 'Genre']).size().reset_index(
    name='Count')

genre_popularity = genre_year_counts.pivot(index='Year', columns='Genre',
                                           values='Count').fillna(0)

genre_popularity = genre_popularity.sort_index()

total_genre_popularity = genre_popularity.sum().sort_values(ascending=False)
print('\nТоп 5 популярных жанров:')
print(total_genre_popularity.head(5))

# Использование библиотеки numpy
ratings = np.array([movie.rating for movie in movies_list])

print("\nАнализ рейтинга:")
print(f"Средний рейтинг: {np.mean(ratings):.2f}")
print(f"Медианный рейтинг: {np.median(ratings):.2f}")
print(f"Стандартное отклонение: {np.std(ratings):.2f}")
print(f"Минимальный рейтинг: {np.min(ratings):.2f}")
print(f"Максимальный рейтинг: {np.max(ratings):.2f}\n")

years = np.array([movie.year for movie in movies_list])

print("Количество фильмов из топ 250 по десятилетиям")
decades = (years // 10) * 10
unique_decades, counts = np.unique(decades, return_counts=True)
for decade, count in zip(unique_decades, counts):
    print(f"{decade}-е: {count}")

# Использование библиотеки matplotlib
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

# График для топ 10 актёров
ax1.bar(range(len(top_actors)), [count for _, count in top_actors],
        align='center')
ax1.set_xticks(range(len(top_actors)))
ax1.set_xticklabels([actor for actor, _ in top_actors], rotation=45,
                    ha='right')
ax1.set_title('Топ 10 популярных актёров')
ax1.set_xlabel('Актёр')
ax1.set_ylabel('Количество фильмов в топ 250')

# График фильмов по десятилетиям
ax2.bar(unique_decades, counts, align='center')
ax2.set_title('Количество фильмов из топ 250 по десятилетиям')
ax2.set_xlabel('Десятилетие')
ax2.set_ylabel('Количество фильмов')
ax2.set_xticks(unique_decades)
ax2.set_xticklabels([f"{decade}s" for decade in unique_decades])

for i, v in enumerate(counts):
    ax2.text(unique_decades[i], v, str(v), ha='center', va='bottom')

plt.tight_layout()
plt.show()
