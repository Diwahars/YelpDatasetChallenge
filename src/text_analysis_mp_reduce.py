from util import *
from mrjob.job import MRJob
import json

class MRStrlenRating(MRJob):

	def mapper(self, _, line):
		# each line is a string and loads reads it into a dictionary
		r = json.loads(line)
		text = r['text']
		# clean up the text
		text = clean_text(text)
		string_length = len(text)
		rating = r['stars']
		yield string_length, rating

if __name__ == "__main__":
	MRStrlenRating.run()