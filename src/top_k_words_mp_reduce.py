from mrjob.job import MRJob
import json
import re

WORD_RE = re.compile(r"[\w']+")

'''
SOURCE NOTE: The list of stop words (below) was adapted from a list posted online
at www.text-analytics101.com/2014/10/all-about-stop-words-for-text-mining.html
'''

stop_words = ["i", "the", "and", "a", "to", "of", "is", "was", "you", "my", "they",
			  "my", "s", "it", "in", "this", "she", "for", "their", "with", "from",
			  "that", "on", "me", "which", "as", "our", "on", "t", "n", "we", "are",
			  "not", "her", "have", "had", "but", "been", "at", "those", "were", "re",
			  "he", "be", "or", "place", "an", "find", "where", "there", "has", "when",
			  "here", "his", "if", "than", "them", "done", "out", "two", "just", "so",
			  "very", "all", "up", "one", "no", "told", "do", "again", "even", "who", "say",
			  "stay", "other", "finally", "don", "most", "much", "section", "trip", "only"]

'''
class MRGetReviewData(MRJob):
	def mapper(self, _, line):
		data = json.loads(line)
		biz_id = data["business_id"]
		text = data["text"]
		yield biz_id, text

	def combiner(self, business, strings):
		text = ""
		for string in strings:
			text+=string + " "
		yield business, text

	def reducer(self, business, strings):
		text = ""
		for string in strings:
			text+=string + " "
		yield business, text

'''
class MRReviewIndex(MRJob):

	def mapper(self, _, line):
		word_list = WORD_RE.findall(line)
		for word in word_list:
			if word not in stop_words:
				yield word, 1

	def combiner(self, word, counts):
		yield word, sum(counts)