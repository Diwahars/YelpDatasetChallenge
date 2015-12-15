import os


# Question 1: What are the top k words in the reviews/tips for each business?

os.system("python src/run_top_k_words.py 3 output/output.txt data/review_subset.json data/tip_subset.json output/temp_data.txt")

# Question 2: How do the ratings of early reviews affect a business's later ratings?

os.system("python src/run_time_improvement_analysis.py output/time_ratings2.txt 6 data/review_subset.json")

# Question 3: Do the star ratings given by reviewers match the polarity of the review text?

os.system("python src/run_text_analysis.py data/review_subset.json")

# Question 4: How does the reviewing/rating behavior of a user compare to the behavior of her friends?

os.system("python src/run_user_friend_analysis.py data/review_subset.json data/tip_subset.json data/user_subset.json")

# Question 5: How does the day of the week affect reviewers' ratings and polarity?

os.system("python src/run_day_polarity_rating_analysis.py data/review_subset.json")
