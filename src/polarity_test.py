from util import *
from mrjob.job import MRJob
import json

class MRPolarityRating(MRJob):

	def mapper(self, _, line):
		# each line is a string and loads reads it into a dictionary
		r = json.loads(line)
		text = r['text']
		# clean up the text
		text = clean_text(text)
		polarity = get_polarity_score(text)
		rating = r['stars']
		yield polarity, rating

if __name__ == "__main__":
	MRPolarityRating.run()