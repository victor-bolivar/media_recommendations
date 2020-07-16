import requests
import json

'''
author : Victor Bolivar De la Cruz
date : 15/07/2020

DESCRIPTION OF THE PROJECT:
This project will take you through the process of mashing up data from two different APIs to make movie recommendations. The TasteDive API lets you provide a movie (or bands, TV shows, etc.) as a query input, and returns a set of related items. The OMDB API lets you provide a movie title as a query input and get back data about the movie, including scores from various review sites (Rotten Tomatoes, IMDB, etc.).

You will put those two together. You will use TasteDive to get related movies for a whole list of titles. You’ll combine the resulting lists of related movies, and sort them according to their Rotten Tomatoes scores (which will require making API calls to the OMDB API.)

To avoid problems with rate limits and site accessibility, we have provided a cache file with results for all the queries you need to make to both OMDB and TasteDive. Just use requests_with_caching.get() rather than requests.get(). If you’re having trouble, you may not be formatting your queries properly, or you may not be asking for data that exists in our cache. We will try to provide as much information as we can to help guide you to form queries for which data exists in the cache.

Your first task will be to fetch data from TasteDive. The documentation for the API is at https://tastedive.com/read/api. '''

## To-do list
# 1. Replace requests_with_caching for requests
# 2. Add an API key 



def get_movies_from_tastedive(name):
	# returs 5 TasteDive results (movies) socciated with the string 'name'
	# in the form a dictionary with just one key : 'Similar'
	
	max_number_of_results = '5'
	base_url = 'https://tastedive.com/api/similar'
	parameters = {}
	parameters['q'] = name
	parameters['type'] = 'movies'
	parameters['limit'] = max_number_of_results

	res = requests.get(base_url, params=parameters)
	res.raise_for_status()
	data = res.json()

	result = []
	for index in range(int(max_number_of_results)):
		result.append(data['Similar']['Results'][index]['Name'])
	return result

def get_related_titles(movies):
	# takes a list of movie titles as input. It gets five related movies for each from TasteDive, extracts the titles for all of them, and combines them all into a single list.
	related_movies = []
	for movie in movies :
		related_movies += get_movies_from_tastedive(movie)
	return list(set(related_movies))

def get_movie_data(movie):
	base_url = 'http://www.omdbapi.com/' #add API key
	parameters = {}
	parameters['t'] = movie
	parameters['r'] = 'json'
	res = requests.get(base_url, params=parameters)
	return res.json()

def get_movie_rating(data):
	#  It takes an OMDB dictionary result for one movie and extracts the Rotten Tomatoes rating as an integer. For example, if given the OMDB dictionary for “Black Panther”, it would return 97. If there is no Rotten Tomatoes rating, return 0.
    if 'Rotten Tomatoes' in data['Ratings'][1].values():
    	return int(data['Ratings'][1]['Value'][:-1])
    else:
    	return 0

def get_sorted_recommendations(movies):
	# It returns a sorted list of related movie titles as output
	related = get_related_titles(movies)
	ratings = [get_movie_rating(movie) for movie in movies]
	movies_info = {}
	for (rating, movie) in list(zip(ratings, related)):
		movies_info[rating] = movie
	sorted_list_movies_rating = sorted(movies_info.items(), reverse=True)
	return [movie_tuple[1] for movie_tuple in sorted_list_movies_rating] 


rating = get_movie_rating(get_movie_data('Black Panther'))

