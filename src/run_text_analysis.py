from text_analysis_mp_reduce import MRStrlenRating
from polarity_test import MRPolarityRating
from util import graph
import sys


'''
	In this file, we examine two questions:

		(1) How reliable is TextBlob, our Natrual Languange Processing API?
			By plotting every review's polarity score (attained with TextBlob) against
			every review's rating -- and by showing that there is a strong positive
			correlation, we are able validate the sentiment analysis function of TextBlob.

		(2) Does the length of the review text have any correlation with the rating the use gives?


	Running this program requires command line parameters:
		python run_text_analysis.py <Reviews Filename to read>

	Sample run code:
		python run_text_analysis.py 'data/review_subset.json'

'''


##########################################################
################						  ################
################ polarity vs. star rating ################
################					   	  ################
##########################################################

'''
	We run through every review in the review json dataset (there are 1.5 million)
	of them. Each line in the json file is one review, so it was very easy for us
	to implement MapReduce on the dataset. With only a mapper in MapReduce, we are
	able to return the polarity score of the text (calculated in mapper with TextBlob),
	and the rating.

	We eventually return a list of tuples: (polarity score, rating) of all reviews
'''

def mk_polarity_rating_list():
	result = []

	job = MRPolarityRating(args = sys.argv[1:])
	with job.make_runner() as runner:
		runner.run()
		for res in runner.stream_output():
			key, value = job.parse_output_line(res)
			tup = (key, value)
			result.append(tup)

	return result


##########################################################
################  length of review text	 #################
################		   vs. 		     #################
################	   star rating       #################
##########################################################

'''
	Exact same idea as above, except that in MapReduce, we yield the
	length of the review text and the rating.

	We eventually return a list of tuples: (length of text, rating) of
	all review texts.
'''


# returns a list of tuples with the following format: (polarity, rating)
def mk_strlen_rating_list():
	result = []

	job = MRStrlenRating(args = sys.argv[1:])
	with job.make_runner() as runner:
		runner.run()
		for res in runner.stream_output():
			key, value = job.parse_output_line(res)
			tup = (key, value)
			result.append(tup)

	return result


##########################################################
################						  ################
################    graphing functions    ################
################					   	  ################
##########################################################


# l is the list of tuples returned as above
def graph_polarity_rating(l):
	x_label = 'Polarity Score'
	y_label = 'Rating (stars)'
	title = 'Polarity of Review Text vs. Reviewer Rating'
	save_filename = 'output/polarity_vs_stars.png'

	graph(l, title, x_label, y_label, save_filename)
	return


# l is the list of tuples returned as above
def graph_strlen_rating(l):
	x_label = 'String Length'
	y_label = 'Rating (stars)'
	title = 'Length of Review Text vs. Reviewer Rating'
	save_filename = 'output/review_length_vs_rating.png'

	graph(l, title, x_label, y_label, save_filename)
	return


if __name__ == '__main__':
	# polarity vs. star rating
	l_1 = mk_polarity_rating_list()
	graph_polarity_rating(l_1)

	# length of text vs. star rating
	l_2 = mk_strlen_rating_list()
	graph_strlen_rating(l_2)
