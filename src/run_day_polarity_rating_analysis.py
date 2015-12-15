from day_polarity_rating_analysis_mp_reduce import *
from util import graph
import sys


'''
	In this file, we examine two questions:

		(1) Does the day of the week have any correlation with the polarity of the review text,
			thus, how happy yelpers are? We analyze this question by plotting the polarity score
			of the review text to the day of the week the review is written.

		(2) Does the day of the week have any correlation with the star rating yelpers give out?
			Similary to above, we analyze this question by plotting the star rating that the
			yelper gives to the day of the week the review is written.


	Running this program requires command line parameters:
		python run_text_analysis.py <Reviews Filename to read>
	
	Sample run code:
		python src/run_day_polarity_rating_analysis.py 'data/review_subset.json'
'''


# This function runs through every single review in the review json dataset
# (there are 1.5 million of then) with MapReduce. Eventually, it returns
# a dictionary with 7 ints as keys (1: Monday, 2: Tuesday, ... 7: Sunday)
# and the value being the list of truple tuples with: (polarity, rating)
# that only belong to the key
def mk_day_polarity_rating_dict():
	result = {}

	job = MRDayPolarityRating(args = sys.argv[1:])
	with job.make_runner() as runner:

		runner.run()

		for res in runner.stream_output():
			key, value = job.parse_output_line(res)
			# key is the dayofweek in int and value is a list of tuples
			# tup = (polarity, rating)
			# there should be only 7 keys: 1, 2, ..., 7
			result[key] = value

	return result


# takes in the dictionary outputed above and returns a dictionary
# with each day (1 - 7) as the key and the value being the list of
# ratings that only belong to that key
def mk_day_rating_dict(day_pol_rating_dict):
	# 1: Monday
	# 2: Tuesday
	# 3: Wednesday
	# 4: Thursday
	# 5: Friday
	# 6: Saturday
	# 7: Sunday
	result = {}
	for i in range(1, 8):
		result[i] = []

	# there are maximum only 7 keys
	for key in day_pol_rating_dict.keys():
		# l is the list of (pol, rating) tuples of the corresponding key(day)
		l = day_pol_rating_dict[key]
		for tup in l:
			result[key].append(tup[1])

	return result
	

# similar idea as above, but the value is now a list of polarity scores (instead of ratings)
def mk_day_polarity_dict(day_pol_rating_dict):
	# 1: Monday
	# 2: Tuesday
	# 3: Wednesday
	# 4: Thursday
	# 5: Friday
	# 6: Saturday
	# 7: Sunday
	result = {}
	for i in range(1, 8):
		result[i] = []

	# there are maximum only 7 keys
	for key in day_pol_rating_dict.keys():
		# l is the list of (pol, rating) tuples of the corresponding key(day)
		l = day_pol_rating_dict[key]
		for tup in l:
			result[key].append(tup[0])

	return result


# general function that computes the average value of the list of polarity scores/star ratings
# makes a tuple: (day, avg_value)
# returns the list of this tuple (there should be a maximum number of 7 of such tuples)
def mk_day_avg_tuple(d):
	result = []
	for key in d.keys():
		l = d[key]
		# safety check just in case that the list is empty
		if len(l) == 0:
			continue
		avg_value = sum(l)/len(l)
		result.append((key, avg_value))
	return result


def graph_day_rating(l):
	x_label = 'Day of Week'
	y_label = 'Rating (stars)'
	title = 'Day of Week vs. Rating (stars)'
	save_filename = 'output/day_of_week_vs_rating.png'
	
	graph(l, title, x_label, y_label, save_filename)
	return


def graph_day_polarity(l):
	x_label = 'Day of Week'
	y_label = 'Polarity Score'
	title = 'Day of Week vs. Polarity Score'
	save_filename = 'output/day_of_week_vs_polarity_score.png'
	
	graph(l, title, x_label, y_label, save_filename)
	return


if __name__ == '__main__':
	day_pol_rating_dict = mk_day_polarity_rating_dict()

	day_rating_dict = mk_day_rating_dict(day_pol_rating_dict)
	day_pol_dict = mk_day_polarity_dict(day_pol_rating_dict)

	l_rating = mk_day_avg_tuple(day_rating_dict)
	l_pol = mk_day_avg_tuple(day_pol_dict)

	graph_day_rating(l_rating)
	graph_day_polarity(l_pol)
