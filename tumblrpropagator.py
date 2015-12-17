import requests, requests_cache, json

#This all uses the tumblr api v1

class tumblrPropagator():
	def __init__(self, baseUrl, scrapeTag):
		self.baseUrl = baseUrl
		self.scrapeTag = scrapeTag

	def _tumblrGetRequest(self, url):
		resp = requests.get(url)

		#We have to do this because tumblr is setup to give us a javascript
		# eval ready thing. It starts with the first 21 chars defining
		# a variable. And then the -2 removes the semicolon.
		return json.loads(resp.text[21:-2])

	def getPosts(self, limit = 10):
		blog = self._tumblrGetRequest(
			"http://%s.tumblr.com/api/read/json?tagged=%s" % (self.baseUrl, self.scrapeTag))

		miscount = 0
		allPosts = []

		for post in blog['posts']:
			if post['type'] == u'photo':
				allPosts.append((None, [post['photo-url-500']], post['photo-caption']))
			elif post['type'] == u'regular':
				allPosts.append((post['regular-title'], None, post['regular-body']))
			else:
				miscount += 1
				#The idea is that the function will call itself again
				# to grab more posts to fill in the blanks. But later.

		return allPosts