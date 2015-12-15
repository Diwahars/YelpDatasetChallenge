Yelp Data Analysis
Final Project for CS 123, Spring 2015
By Davis Tsui & Rachel Whaley


Our code is organized into sets of files that answer particular questions about our data.


Question 1: What are the top k words in the reviews/tips for each business?

	files:

		run_top_k_words.py
			^This program reads in review and tip data, indexes the text of all reviews and tips to find the top k words for each business, compares these words to the categories that yelp has assigned to the business, and makes suggestions for additional category tags (words in the top k words that are not already a category). These suggestions are writtn to a file called suggestions.txt

		top_k_words_mp_reduce.py:
			^This file contains MapReduce functions for run_top_k_words.py.


Question 2: How do the ratings of early reviews affect a business's later ratings?

	files:
		run_time_improvement_analysis.py
			^This program breaks the reviews for each business into an early set and a later set chronologically, compares the average ratings for the early sets with the average ratings of the later sets to see if there is generally improvement or decline in ratings.

		time_improve_mp_reduce.py
			^This file contains MapReduce functions for run_time_improvement_analysis.py.


Question 3: Is there a positive correlation between the polarity score of each review text and the star rating given by the reviewer. In other words, how realiable is the sentiment analysis of our Natural Language Processing API?

	files:
		run_text_analysis.py
			^Using MapReduce, this program finds a reviewer's star rating and the polarity of the text of the review (as identified by TextBlob's sentiment analysis), and outputs a plot of the correlation between polarity and rating.

		text_analysis_mp_reduce.py
			^This file contains MapReduce functions for run_text_analysis.py.


Question 4: Does the length of the review text have any correlation with the rating the use gives?

	files:
		run_text_analysis.py
			^This program finds the length of a review text (thank you strlen) and the star rating of the test as give as part of the review json file line, and outputs a plot of the correlation between length of the review test and rating.

		text_analysis_mp_reduce.py
			^This file contains MapReduce functions for run_text_analysis.py.


Question 5: Does the day of the week have any correlation with the star rating of the review text?

	files: 
		run_day_polarity_rating_analysis.py
			^This program categorizes reviews by day of the week (Monday-Sunday), finds the star rating of each review, and outputs a plot of star rating by day of the week.
		day_polarity_rating_analysis_mp_reduce.py
			^This file contains MapReduce functions for run_day_polarity_rating_analysis.py.


Question 6: Does the day of the week have any correlation with the polarity of the review text, thus, how happy yelpers are?

	files: 
		run_day_polarity_rating_analysis.py
			^This program categorizes reviews by day of the week (Monday-Sunday), finds the polarity of each review using TextBlob's sentiment analysis, and outputs a plot of the 7 average review polarity score by day of the week.

		day_polarity_rating_analysis_mp_reduce.py
			^This file contains MapReduce functions for run_day_polarity_rating_analysis.py.


Question 7: How likely is that a yelper's friend has also visited at least one of the restaurants/businesses that the yelper has left a review/tip for. A person is considered having visited the restaurant/business if the person has once left a review/tip for the restaurant/business.

	files:
		run_user_friend_analysis.py
			^This program runs through the user json dataset and looks at every user individually. It then finds the list of the restaurant that the user has
			been to and then it will match it to the list of restaurant that the yelper's
			friends (once again, we look at friends one by one here). If there is
			intersection (thus, common ground) between the two sets of restaurants,
			then the individual event is considered a success. Eventually, this program
			returns a success percentage of finding at least one of yelper's friends who
			shares at least one restaurant with him/her.

		user_friend_analysis_mp_reduce.py
			^This file contains MapReduce functions for run_user_friend_analysis.py


Additional item:

	(1) README.txt is this file.
	(2) src (folder) contains all the source code for this project as described above
	(3) data (folder) contains subset datafiles for demonstration and testing use.
	(4) run_all.py: python run_all.py will run all the source codes and output the
					correpsonding graphs or prints to the terminal.
	(5) final_writeup.txt contains our final writeup for this project, describing our
		research questions, hypotheses, methods, results, and challenges encountered.