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

	def _getPostsHelper(self, startPos = 0, limit = 10):
		blog = self._tumblrGetRequest(
			"http://%s.tumblr.com/api/read/json?tagged=%s&start=%s&num=%s" % (self.baseUrl, self.scrapeTag, startPos, limit))

		miscount = 0
		allPosts = []

		for post in blog['posts']:
			if post['type'] == u'photo':
				allPosts.append((None, [post['photo-url-500']], post['photo-caption'], post['url']))
			elif post['type'] == u'regular':
				allPosts.append((post['regular-title'], None, post['regular-body'], post['url']))
			else:
				miscount += 1
				#The idea is that the function will call itself again
				# to grab more posts to fill in the blanks. But later.

		return allPosts


	def getPosts(self, startPos = 0, limit = 10):
		allPosts = self._getPostsHelper(startPos, limit)

		#Do a quick check to see if there are posts beyond the horizon.
		offset = 0
		if startPos == 0:
			offset = limit
		else:
			offset = startPos + limit

		singlePost = self._getPostsHelper(offset, 1)

		hasMore = True
		if singlePost == []:
			hasMore = False

		return allPosts, hasMore