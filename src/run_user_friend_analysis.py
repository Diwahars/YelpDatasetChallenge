from user_friend_analysis_mp_reduce import *
from multiprocessing import Pool
import json
import sys

'''
	In this file, we examine the question:

		(1) How like is it that a friend of a yelper has also once visited the restaurant that the yelper
			left a review for. Here, we define visiting with the fact that s/he has once left a review/tip
			for the business.


	Running this program requires command line parameters:
		python run_text_analysis.py <Reviews Filename to read> <Tips Filename to read> <Users Filename to read>
	
	Sample run code:
		python src/run_user_friend_analysis.py 'data/review_subset.json' 'data/tip_subset.json' 'data/user_subset.json'
'''


# adopted from the code snippet from Lectures 4 & 5
# used for multi processing
# divides the file into 'chunks' chunks
def find_file_ranges(fname, chunks):
    f = open(fname)

    f.seek(0,2)
    fsize = f.tell()

    ranges = []
    chunk_size = fsize / chunks
    start = 0
    for i in range(chunks):
        f.seek(start + chunk_size)
        l = f.readline()
        end = min(start + chunk_size + len(l) - 1, fsize)
        ranges.append( (start, end) )
        start = end + 1

    f.close()
    return ranges


# returns a dictionary with each user_id as the key and the value as
# the list of restaurants that the user has gone to
def find_restaurants():
	r = {}

	# first map reduce job: goes through the review json file and
	# appends the business id of the business the user has left a review for
	# feed in the review json file
	# job = MRReview(args = ['-r', 'emr', sys.argv[1:]])
	review_job = MRFindRestaurant(args = sys.argv[1:])
	with review_job.make_runner() as runner:
		runner.run()
		for res in runner.stream_output():
			key, value = review_job.parse_output_line(res)
			# key is user_id and value is business_id
			if r.has_key(key):
				r[key].append(value)
			# doesn't have the key, declare the empty list and put the value in it
			else:
				r[key] = [value]
	
	# go through tips now
	tip_job = MRFindRestaurant(args = sys.argv[2:])
	with tip_job.make_runner() as runner:
		runner.run()
		for res in runner.stream_output():
			key, value = tip_job.parse_output_line(res)
			if r.has_key(key):
				r[key].append(value)
			# doesn't have the key, declare the empty list and put the value in it
			else:
				r[key] = [value]

	# now, r is a dictionary with every user (that we have information on)
	return r



# this function takes in the library outputed by the function above
# if we have the time, we can potentially do this by geo-location
# i'm going to use multi-processing here
def find_percent_common_restaurant(args):
	filename = args[0]
	user_rest_dict = args[1]
	my_range = args[2]

	print type(user_rest_dict)
	print len(user_rest_dict.keys())

	# every time a user is being looked up and compared to his/her friends, total += 1
	total = 0;
	# if at least one friend has been to the same restaurant as the user then, success += 1
	success = 0;
	# we return the tuple (success, total) at the end

	f = open(filename, 'r')
	f.seek(my_range[0])
	for line in f:
		r = json.loads(line)
		user = r['user_id']
		# friends is a list of user_ids
		friends = r['friends']

		# if user is not in the user_rest_dict, skip
		if not user_rest_dict.has_key(user):
			continue
		# one user is being read
		total += 1
		print total

		# user_restaurants need to be in a list for the intersection function later
		user_restaurants = set(user_rest_dict[user])
		
		for friend in friends:
			if not user_rest_dict.has_key(friend):
				print 'friend not in dict'
				continue

			friend_restaurants = set(user_rest_dict[friend])

			intersect = set.intersection(*[user_restaurants, friend_restaurants])
			if len(intersect) != 0:
				success += 1
				break
	f.close()

	result = (success, total)
	return result


# k is the number of processes/chunks that you want to 
def find_perc_common_rest_wrapper(d):
	fname = 'data/user_subset.json'
	# spawn 4 instances
	nchunks = 4
	p = Pool(nchunks)
	# divide the file into 4 chunks
	franges = find_file_ranges(fname, nchunks)

	args = zip([fname]*nchunks, [d]*nchunks, franges)

	res = p.map(find_percent_common_restaurant, args)

	success = 0
	total = 0

	for result in res:
		print type(result)
		print result[0]
		print result[1]
		success += result[0]
		total += result[1]

	if total == 0:
		percentage = 0.0

	else:
		percentage = success/total

	return percentage

if __name__ == '__main__':
	user_rest_dict = find_restaurants()
	find_perc_common_rest_wrapper(user_rest_dict)
	
