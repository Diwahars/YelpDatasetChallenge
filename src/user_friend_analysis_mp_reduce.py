from mrjob.job import MRJob
import json

# for each review or tip, returns the tuple: (user_id, business_id)
class MRFindRestaurant(MRJob):

	def mapper(self, _, line):
		r = json.loads(line)
		keys = r.keys()
		if 'user_id' and 'business_id' in keys:
			user_id = r['user_id']
			business_id = r['business_id']
			yield user_id, business_id
