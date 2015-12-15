from textblob import TextBlob
import matplotlib.pyplot as plt
import re


'''
	Helper functions that are common to many files
'''


def clean_text(text):
	# clean the text and make a list of those words
	text_clean = re.findall("[a-zA-Z]\w*", text.lower())
	# then turn the list of cleaned words back into a string
	text_clean_s = ""
	for word in text_clean:
		text_clean_s = text_clean_s + word + " "

	return text


# returns the polarity score of a given string of text
def get_polarity_score(text):
	t = TextBlob(text)
	polarity_score = t.sentiment.polarity
	return polarity_score

def graph(l, title, x_label, y_label, save_filename):
	plt.scatter(*zip(*l))
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.title(title)
	plt.savefig(save_filename)
	plt.close()
	print "Scatterplot of results saved to " + save_filename
	return
