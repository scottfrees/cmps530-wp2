import csv
import json
import statistics
import time

ratings_file = "data/ratings.csv"
frequent_threshold = 10000


def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


def make_movie_dictionary(row):
    if row[2] == "(no genres listed)":
        genres = []
    else:
        genres = row[2].split("|")
    tags = list()
    ratings = list()
    tokens = row[1].split("(")
    title = "(".join(tokens[:-1])
    year_s = intTryParse(tokens[-1].split(")")[0])
    if year_s[1]:
        year = year_s[0]
    else:
        year = 0
        title = row[1]
    return {
        "id": row[0],
        "title": title.strip(),
        "year": year,
        "ratings": ratings,
        "tags": tags,
        "genres": genres,
    }


def find_movie_by_id(movies, id):
    for movie in movies:
        if movie["id"] == id:
            return movie
    return None


print("Loading movies...")
movies = list()
with open("data/movies.csv", "r") as csvfile:
    next(csvfile)
    movie_reader = csv.reader(csvfile)
    for row in movie_reader:
        movie = make_movie_dictionary(row)
        movies.append(movie)


print("Loading ratings...")
start = time.time()
with open(ratings_file, "r") as csvfile:
    next(csvfile)
    ratings_reader = csv.reader(csvfile)
    for row in ratings_reader:
        movie_id = row[1]
        movie = find_movie_by_id(movies, movie_id)
        if movie == None:
            print("NO MOVIE")
        else:
            ratings = movie["ratings"]
            ratings.append(float(row[2]))
now = time.time()
print("Time to load ratings:  ", str(now - start), "seconds")

print("Loading tags...")
start = time.time()
with open("data/tags.csv", "r") as csvfile:
    next(csvfile)
    tags_reader = csv.reader(csvfile)
    for row in tags_reader:
        movie_id = row[1]
        movie = find_movie_by_id(movies, movie_id)
        if movie == None:
            print("NO MOVIE")
        else:
            tags = movie["tags"]
            if row[2] not in tags:
                tags.append(row[2])
now = time.time()
print("Time to load tags:  ", str(now - start), "seconds")

print("Calculating average ratings for each movie...")
for movie in movies:
    if len(movie["ratings"]) > 0:
        movie["average_rating"] = statistics.mean(movie["ratings"])
    else:
        movie["average_rating"] = None


#####################################################
##  Genre Stats
#####################################################
genre_stats = dict()
for movie in [m for m in movies if m["average_rating"] != None]:
    num = str(len(movie["genres"]))
    if num in genre_stats:
        genre_stats[num].append(movie["average_rating"])
    else:
        genre_stats[num] = [movie["average_rating"]]

with open("solution/genre-ratings.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Number of Genres", "Average Movie Rating"])
    for num in sorted(genre_stats.keys(), key=lambda k: (int(k))):
        writer.writerow([num, statistics.mean(genre_stats[num])])
#####################################################


#####################################################
# Tags
#####################################################
tags = dict()
for movie in [m for m in movies if m["average_rating"] != None]:
    for tag in movie["tags"]:
        if tag in tags:
            tags[tag].append(movie["average_rating"])
        else:
            tags[tag] = [movie["average_rating"]]

common_tags = []
for tag in tags:
    if len(tags[tag]) > 100:
        common_tags.append((tag, statistics.mean(tags[tag])))

good_tags = sorted(common_tags, key=lambda k: (k[1]), reverse=True)[:20]

with open("solution/top-tags.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Tag", "Average Movie Rating"])
    for v in sorted(good_tags):
        writer.writerow(v)

#####################################################

#####################################################
# Frequently Rated
#####################################################
movie_list = sorted(
    [m for m in movies if len(m["ratings"]) >= frequent_threshold],
    key=lambda k: (k["average_rating"], k["year"], k["title"]),
    reverse=True,
)

# At this point we don't need all the ratings anymore, lets
# collapse that field into the # of ratings - otherwise the
# CSV/JSON we create later will be way too big to be useful!
movie_list = [
    {
        "id": m["id"],
        "title": m["title"],
        "year": m["year"],
        "average_rating": m["average_rating"],
        "ratings": len(m["ratings"]),
        "tags": m["tags"],
        "genres": m["genres"],
    }
    for m in movie_list
]


with open("solution/frequently-rated.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(
        ["ID", "Title", "Year", "Avg. Rating", "# of Ratings", "Genres", "Tags"]
    )
    for movie in movie_list:
        writer.writerow(
            [
                movie["id"],
                movie["title"],
                movie["year"],
                movie["average_rating"],
                movie["ratings"],
                " | ".join(movie["genres"]),
                " | ".join(movie["tags"]),
            ]
        )

with open("solution/frequently-rated.json", "w") as fout:
    json.dump(movie_list, fout)
#####################################################
