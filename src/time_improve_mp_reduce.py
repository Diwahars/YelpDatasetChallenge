from mrjob.job import MRJob
import json
import re

class MRTimeCorrelation(MRJob):

	def mapper(self, _, line):
		# mapper will output business id, "date rating"
		r = json.loads(line)
		biz_id = r["business_id"]
		rating = float(r["stars"])
		year = r["date"][:4]
		month = r["date"][5:7]
		day = r["date"][-2:]
		full_date = year+month+day
		stringify = full_date+ " " + str(rating)
		yield biz_id, stringify

	def combiner(self, biz_id, data):
		yield biz_id, list(data)

	def reducer(self, biz_id, data):
		# the final output here is the list of "date rating" strings for each business
		yield biz_id, list(data)
