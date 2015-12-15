from util import *
from mrjob.job import MRJob
import datetime
import json


class MRDayPolarityRating(MRJob):

	def mapper(self, _, line):
		# each line is a string and loads reads it into a dictionary
		r = json.loads(line)
		text = r['text']
		# clean up the text
		text = clean_text(text)
		polarity = get_polarity_score(text)
		rating = r['stars']
		
		tup = (polarity, rating)

		date = r['date']
		temp_date_l = date.split('-')
		year = int(temp_date_l[0])
		month = int(temp_date_l[1])
		day = int(temp_date_l[2])
		d = datetime.date(year, month, day)
		weekday = d.isoweekday()

		yield weekday, tup

	# skip combiner here because there is nothing to distill within each node

	# reduce and return the list of tuples
	# perfect use of map reduce
	def reducer (self, dayofweek, tups):
		tups_list = list(tups)
		yield dayofweek, tups_list
