from top_k_words_mp_reduce import MRReviewIndex
import sys
import json
import re

'''
Running this program requires command line parameters:
	python run_yelp_data_test.py <Desired Vale of K> <Filename for Writing Output> 
								<Reviews Filename to read> <Tips Filename to read> "temp_data.txt"

	arg 1 is: Desired Value of K (the top K words you want to get for each business)
	arg 2 is: Filename for Writing Output (usually output.txt; note that this program appends
			  data to this file, rather than overwriting it, so if you want to see output from the
			  most recent run, delete the old output file, write to a new one, or scroll down to the bottom)
	arg 3 is: review data file you want to index.
	arg 4 is: tips data file you want to index
	arg 5 is: temp_data.txt . It always has to be exactly that, due to the fact that MapReduce has
			  to take in data from the command line.

	Sample run code:

	python run_top_k_words.py 1 output.txt data/review_subset.json data/tip_subset.json temp_data.txt
	python run_top_k_words.py 3 output2.txt data/review_subset.json data/tip_subset.json temp_data.txt

'''

WORD_RE = re.compile(r"[\w']+")


def create_biz_review_txt(reviews_filename, tips_filename, output_filename):
	'''
	This fn takes in the names of the reviews and tips json files, and outputs a text 
	file with a json dictionary in the following format: 
	{ business_id: {'text': "text of all reviews/tips"}, biz_id_2: 'text': "some text" } ... }
	'''
	reviews_by_biz = {}
	with open(reviews_filename, 'r') as reviews_file:
		for review in reviews_file:
			# review is a string and loads reads it into a dict
			r = json.loads(review)
			text = r["text"]

			# clean the text and make a list of those words
			text_clean = re.findall("[a-zA-Z]\w*", text.lower())

			# then turn the list of cleaned words back into a string
			text_clean_s = ""
			for word in text_clean:
				text_clean_s = text_clean_s + word + " "

			# add the place to the dict, or append its entry
			place = str(r["business_id"])
			if place in reviews_by_biz:
				reviews_by_biz[place]["text"] += ' ' + text_clean_s
			else:
				reviews_by_biz[place] = {}
				reviews_by_biz[place]["text"] = text_clean_s

	# now add tips to reviews_by_biz
	with open(tips_filename) as tipfile:
		for tip in tipfile:
			data = json.loads(tip)
			tip_text = data["text"]
			tip_clean = re.findall("[a-zA-Z]\w*", text.lower())
			tip_clean_s = ""
			for word in tip_clean:
				tip_clean_s = tip_clean_s + word + " "
			biz = data["business_id"]
			if reviews_by_biz.has_key(biz):
				reviews_by_biz[biz]["text"] += ' ' + tip_clean_s
			else:
				reviews_by_biz[biz] = {}
				reviews_by_biz[biz]["text"] = tip_clean_s

	# for the first 500 lines, there are 39 unique keys (businesses)
	with open(output_filename, 'w') as f:
		json.dump(reviews_by_biz, f)
	return

def top_k_by_biz(top_k_filename, suggestion_file, storage_filename, k):
	'''
	Add explanatory comment here
	'''
	# make sure output files are empty to start, since we append data later
	with open(top_k_filename, 'w') as f:
		f.write('')
	with open(suggestions_file, 'w') as f:
		f.write('')
	
	biz_file = open(storage_filename, 'r')

	# now we go through each business's information
	json_data = json.load(biz_file)
	text_only = ""
	for item in json_data:
		text_only = json_data[item]["text"]
		biz_name = item

		# Now we write this business's information to a temporary file.
		# temp_data.txt gets overwritten for each business.
		# This serves as a temporary text that gets passed into map reduce.
		temp_file = open('output/temp_data.txt', 'w')
		temp_file.write(text_only)
		temp_file.close()

		# now we feed that temp file into map reduce
		# to perform top-k words analysis and filtering on each review set
		job = MRReviewIndex(args=sys.argv[5:])
		with job.make_runner() as runner:
			# Run the job
			runner.run()
			
			l = []
			# Process the output
			for line in runner.stream_output():

				key, value = job.parse_output_line(line)
				# values first, and then key for sorting easily by frequency
				l.append((value, key))

			l.sort(reverse = True)

		top_k_words = ""

		# it is possible that with all the stop words that we have, 
		# there will not be k words left, so we take the min
		k = min(k, len(l))

		# then we find the top k words and write them to a file
		for i in range(k):
			top_k_words += str(l[i][1]) + " "
		with open(top_k_filename, 'a') as output_file:
			output_file.write(biz_name + ": " + top_k_words + "\n")

	biz_file.close()

def create_cats_dict(filename):
	'''
	This fn takes the file of businesses and returns a dictionary of the categories
	that yelp has assigned to the business.
	'''
	cats_dict = {}
	with open(filename, 'r') as f:
		for biz in f:
			data = json.loads(biz)
			biz_id = data["business_id"]
			cats = data["categories"]
			cats_dict[str(biz_id)] = []
			cats_string = ""
			for item in cats:
				cats_string += str(item) + " "
			cats_string2 = ""
			for item in cats_string:
				diff = item.split("&")
				for i in diff:
					cats_string2 += i + " "
			cats_sep = WORD_RE.findall(cats_string.lower())
			for cat in cats_sep:
				cats_dict[str(biz_id)].append(cat)
	return cats_dict

def make_suggestions(biz_cats, top_k_filename):
	'''
	This fn takes in the existing categories of each business and the top k words
	among reviews for each business. It writes to a file "suggestions.txt" any words
	that appear in the top k that are not already a category (these are the suggestsions
	for additional category tags).
	'''
	data_dict = {}
	with(open(top_k_filename, "r")) as readfile:
		count = 0
		for line in readfile:
			# grab the top k words from file
			count +=1
			data = line.split(':')
			biz_id = data[0]
			top_k_words = data[1].split()
			for word in top_k_words:
				word = word.lower()
			# find the actual categories
			cats = []
			if biz_id in biz_cats:
				cats = biz_cats[biz_id]
			# find any words in top k that do not appear in actual categories
			suggested_cats = []
			for word in top_k_words:
				if word not in cats:
					# many of yelp's categories are plural (e.g. "bars") so we check for that here
					if (word + "s") not in cats:
						suggested_cats.append(word)
			# create a dictionary as value for each business as key
			data_dict[biz_id] = {'suggested': suggested_cats, 'actual': cats}
	# write all suggestions to file
	with open("output/suggestions.txt", "w") as suggestion_file:
		json.dump(data_dict, suggestion_file)

	return

if __name__ == '__main__':

	if len(sys.argv) != 6:
		print "error: proper format is "
		print "python run_yelp_data_test.py <Desired Vale of K> <Filename for Writing Output> <Reviews Filename to read> <Tips Filename to read> temp_data.txt"
		print "An example: python run_top_k_words.py 3 output2.txt data/review_subset.json data/tip_subset.json temp_data.txt"
		sys.exit()

	k = int(sys.argv[1])
	top_k_filename = str(sys.argv[2])
	review_datafile = str(sys.argv[3])
	storage_filename = 'output/biz_review.txt'
	tips_filename = str(sys.argv[4])
	suggestions_file = "output/suggestions.txt"

	# here we pile all the data into biz_review.txt.
	create_biz_review_txt(review_datafile, tips_filename, storage_filename)

	# now we find the top k words for each business and write them to top_k_filename
	top_k_by_biz(top_k_filename, suggestions_file, storage_filename, k)

	# the following gives us "suggestions" for more category tags
	# a "suggestion" is something that came up in the top k that is not already in the categories
	biz_cats = create_cats_dict('data/business_subset.json')
	make_suggestions(biz_cats, top_k_filename)
	print "Suggested categories/tags have been written to the file output/suggestions.txt"
