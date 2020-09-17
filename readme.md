# Weekly Project 2
This week's project will have you analyze a large data set consisting of movies, tags applied to movies (descriptive), and user entered ratings.  The data set is commonly used in Machine Learning based recommendation systems (think Netflix).  You will compute three different result sets from the data.

This is a somewhat open-ended assignment in terms of *how your code* is structured - however my recommendation is to make smart use of lists, dictionaries, and many of the other programming structures you've been learning/reviewing this week.  **The only restriction for this week is that I ask you not to use `numpy`, `pandas`, or any other Python library beyond `csv`, and `statistics` for [computing the mean of a list](https://docs.python.org/3/library/statistics.html).**

## Get the project
From your terminal / command line, navigate to a directory where you'd like to store your work.  Then, clone the assignment's github repository and `cd` into the directory to begin working.

```
git clone https://github.com/scottfrees/cmps530-wp2.git
cd cmps530-wp2
```

## Get the data
```
dvc pull
```
I have provided you three input files in the `/data` directory:
- movies.csv
- ratings.csv
- tags.csv

These files are fairly self-explanatory.  `movies.csv` is the core file - it lists lots of movies, and provides genre classifications for most.

`ratings.csv` are user-supplied ratings.  Each row accounts for a single rating, and can be connected to the movie being rated using the second column.

`tags.csv` is similar, each row is a user-applied tag (third column) to a movie (second column).

## Analyze the Data
First you need to load the data and store it in a workable way.  While you are free to use any approach you wish, here's my recommendation:

- Create a dictionary, whose keys are movie id's, and values are dictionaries with the full movie information (id, title, year, genres). 
- The genres value for each movie dictionary should be a proper list or tuple - not a string delimited with | characters.
- Add an empty tags and ratings list to each movie dictionary.
- Load ratings csv file, and for each rating row, look up the movie dictionary using the movie id in the rating row.  Append the rating (you just need the number, not the timestamp) to the correct movie's rating list.
- Follow the same approach with tags - building a list of tags within each movie dictionary.  **Important**, some tags were applied to movies many times by different people, make sure you don't place duplicate tags into a movie's tag list.
- Compute the average rating for each movie, and store that value directly in each movie dictionary (you'll need this for the analysis)

At the end, you should have something structured like this:

```json
{
    "318": {
        "id": "318",
        "title": "Shawshank Redemption, The",
        "year": 1994,
        "average_rating": 3,
        "ratings": [2.4, 3.4, 3.2],
        "tags": ["freedom", "hope"],
        "genres": ["Crime", "Drama"]
    },
    "858": {
        "id": "858",
        "title": "Godfather, The ",
        "year": 1972,
        "average_rating": 3,
        "ratings": [2.4, 3.4, 3.2],
        "tags": ["italian mafia", "italy"],
        "genres ": ["Crime", "Drama"]
    }
    ... many more
}
```

Once you've loaded your dictionary (key are movie ids) of dictionaries (one dictionary for each movie), you can convert that into a list if you would like - or you can continue to use it as a dictionary.

*Note, this is my recommended way to load the data, and it makes heavy used of dictionaries.  The reason dictionaries are important is that you must look up data (movies) while processing the millions of ratings and tags.  Dictionaries are good for lookup (by movie id). If you go another direction, you might find that your program takes hours to run!*

### Tips on Data Loading and Cleaning
1. The ratings file is really large - it's going to take a long time to map ratings to the movies themselves.  A good idea would be to make a temporary ratings file, with much less ratings (just take the first few thousand lines).   Work on the smaller data, and then move to the larger data!

2.  You must parse the title (year) column in the `movie.csv` file so you can hold title and year as separate values within each movie dictionary.  Some movies titles have () in them - be careful when parsing title/year!  

3. Years are missing for many movies.  Make sure when parsing the title/year you account for these, and retain the correct title.  You can put 0 for the year.

4. Some movies don't have any genres - make sure each movie that has no genres correctly has an empty list in it's genres property.

5. You want to convert years from strings to integers.  The below code might be helpful, given that sometimes you aren't sure if you have an integer or not.

```python
def intTryParse(value):
    try:
        return int(value)
    except ValueError:
        return 0 # if the year can't be parsed, just return 0
```

### Part 1: Average Ratings and Number of Genres  
Some movies have no genres, others have one, and others have many assigned to them.  Group movies into categories based on the number of genres assigned to them (i.e. 0, 1, 2, 3,....) and compute the **average** rating of movies in each category.  Output this data as a **csv** file, where the first column is the number of genres and the second column is the average movie rating.

Remember, there were some movies that didn't have any ratings.  Be very careful with these - they should not contribute to the average rating within a genre category!

**Important**:  If there are 5 movies that have 2 genres (for example), to compute the average rating for movies  with 2 genres, I want you to average the 5 average ratings found in the 5 movies.  This is different than simply averaging all the ratings - as some movies have a lot more ratings than others.  

**I have provided you with the correct output**, compare your output to `solution/genre-ratings.csv`.

### Part 2:   Top Rated Tags
Most movies have tags associated with them.  For this analysis, you need to pivot the data, and calculate the average movie rating for each tag.  Calculate average rating using the same method as in Part 2 - take the average of the average ratings on each movie.  Filter the data to include only tags associated with 100 or more movies (which have ratings), and output to top 20 tags in a CSV file, sorted (highest to lowest) by average rating.

**Tip**:  Create a dictionary to hold tags and a list of ratings (the average rating of each movie with the given tag).  Cycle through each movie, each tag within each movie.  For each tag, look it up in the dictionary.  If present, add the movie's rating to the list associated with the tag.  If not, add the tag to the dictionary with a list containing the single movie's rating.

Compare your solution with `solution/top-tags.csv`.

### Part 3:  Frequently Rated Movies
Filter movies to include only movies with at least 10,000 ratings.  Sort the movies by average rating (highest to lowest).

Create a CSV file containing the following data:
ID,Title,Year,Avg. Rating,# of Ratings,Genres,Tags
- Column 1: Movie ID
- Column 2: Title
- Column 3: Year
- Column 4: Average Rating
- Column 5: # of Ratings
- Column 6: Genres (single string, with genres delimited by | character)
- Column 7: Tags (single string, with genres delimited by | character)

Compare your output with `solution/frequently-rated.csv`.

## Takeaways
Consider the following question:
  - What would you change about the format of the original data as it was provided?
