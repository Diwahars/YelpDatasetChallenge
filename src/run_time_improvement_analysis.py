import json
import sys
from scipy import stats
import numpy as np
import mrjob
import matplotlib.pyplot as plt
from time_improve_mp_reduce import MRTimeCorrelation
from pylab import *

################################################
################## Question ####################
################################################
######## Do negatives reviews or ratings #######
######## lead to improvement over time?   ######
################################################

'''
Command line arguments: 
	
	1) file to write average review rating to
	2) partition value for time comparison. For this positive integer value of n, where 
	   1 < n < 10, our code will compute and compare the average rating of the first 1/n reviews
	   and the later ((n-1)/n) reviews for each business, to check for improvement
	   over time. We think that 6 is a good place to start (comparing the first sixth
	   of a business's reviews to the more recent five-sixths).
	3) file to read review data from

Example run command:
	python run_time_improvement_analysis.py time_ratings2.txt 6 data/review_subset.json
'''

def partition_reviews(write_file):
	'''
	This fn takes in review data from the command line, puts reviews in chronological order, 
	partitions them into an early set and a later set, takes the average rating of each set
	of reviews for each business, and writes to a file the business and each of its averages.
	'''
	output = open(write_file, 'w')

	job = MRTimeCorrelation(sys.argv[3:])
	with job.make_runner() as runner:
		# Run the job
		runner.run()
		# Process the output
		for line in runner.stream_output():
			biz, reviews_list = job.parse_output_line(line)
			
			# since the data is stored in strings, we need to parse it
			reviews_ordered = sorted(reviews_list[0])
			num_reviews = len(reviews_ordered)
			reviews_ordered_list = []
			for item in reviews_ordered:
				pieces = item.split(" ")
				tup = (pieces[0], float(pieces[1]))
				reviews_ordered_list.append(tup)

			# now checking the ratings of the first reviews against the rest of them

			# don't analyze if the sample of reviews is too small
			if len(reviews_ordered_list) < 5:
				continue
			# ensure that small-ish samples of reviews always have at least 2 in the threshold
			elif (len(reviews_ordered_list) < 20) and (partition > 5):
				threshold = 2
			else:
				threshold = len(reviews_ordered_list)/partition

			first_reviews = reviews_ordered_list[:threshold]
			later_reviews = reviews_ordered_list[threshold:]
			first_sum = 0
			for i in range(len(first_reviews)):
				first_sum += float(first_reviews[i][1])
			later_sum = 0
			for i in range(len(later_reviews)):
				later_sum += float(later_reviews[i][1])
			first_reviews_ave = first_sum/float(len(first_reviews))
			later_reviews_ave = later_sum/float(len(later_reviews))
			output.write(biz + ", " + str(first_reviews_ave) + ", " + str(later_reviews_ave) + ", " + str(num_reviews) +"\n")

	output.close()
	return

def correlate(datafile, partition):
	'''
	This fn reads in data of the format business_id, early_rating_ave, later_rating_ave
	and outputs the slope, r value (correlation coefficient), and a plot of the data with
	the linear regression line. Plot gets saved to time_analysis_results.png.
	'''
	ratings_data = open(datafile, 'r')
	x_vals = []
	y_vals = []
	for line in ratings_data:
		line_list = line.split(", ")
		x_vals.append(float(line_list[1]))
		y_vals.append(float(line_list[2]))
	x = np.array(x_vals)
	y = np.array(y_vals)
	slope, intercept, r, p, slope_std_err = stats.linregress(x,y)

	print "Regression results: " + "Slope: " + str(slope) + " R value: " + str(r)
	print "y = " + str(slope) + "x + " + str(intercept) 

	fit = np.polyfit(x, y, deg=1)
	plt.plot(x, fit[0]*x + fit[1], color='red')
	plt.scatter(x,y)
	x_label = "Average Rating of Early Reviews (First 1/" + str(partition) + " Reviews)"
	y_label = "Average Rating of Later Reviews (Most Recent " + str(partition-1) + "/" + str(partition) + " Reviews)"
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.xlim([0,5.5])
	plt.ylim([0,5.5])
	plt.title("Early Average Reviewer Rating vs. Later Average Reviewer Rating")
	#plt.show() 
	plt.savefig('output/time_analysis_results.png')
	plt.close()
	print "Scatterplot of correlation results saved to output/time_analysis_results.png"
	return

if __name__ == '__main__':

	write_file = sys.argv[1]
	partition = int(sys.argv[2])
	read_file = sys.argv[3]

	# Now we partition the reviews for each business into an early set and a later set.
	partition_reviews(write_file)

	# Now we will output a graph of the correlation and the R-squared value between
	# earlier reviews and later reviews of the business.
	correlate(write_file, partition)


