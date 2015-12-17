import requests, requests_cache, datetime, base64

#Gotta cache that shit, because otherwise we reach the hourly rate limit of 60 pretty quickly.
#With an authenticated request, that goes up to 5000, but I still don't like calling it
#every single time. This is also a lot faster.
requests_cache.install_cache('request_cache1', backend='sqlite', expire_after=3600)

def convertTime(gitTimestamp):
	return datetime.datetime.strptime(gitTimestamp, "%Y-%m-%dT%H:%M:%SZ").strftime('%b %d, %Y')

class GitHubPropagator:
	def __init__(self, userAgent, gitUser):
		self.userAgent = userAgent
		self.gitUser = gitUser

	def _getRequest(self, url):
		resp = requests.get(url, headers = {"User-agent": self.userAgent})
		return resp.json(), resp.status_code

	def _formatProject(self, project):
		isOwner = False

		if project['owner']['login'] == self.gitUser:
			isOwner = True

		return {"name": project['name'], "lastPush": convertTime(project['pushed_at']),
				"created": convertTime(project['created_at']), "forkCount": project['forks'],
				"description": project['description'], "url": project['html_url'], "owner": isOwner}

	def getReadme(self, name):
		url = "https://api.github.com/repos/%s/%s/readme" % (self.gitUser, name)
		readme, status = self._getRequest(url)

		if status != 200:
			return None

		return base64.b64decode(readme['content'])

	def getProject(self, name):
		url = "https://api.github.com/repos/%s/%s" % (self.gitUser, name)
		repo, status = self._getRequest(url)

		if status != 200:
			return None

		return self._formatProject(repo)

	def getAllProjects(self):
		repos, status = self._getRequest("https://api.github.com/users/%s/repos" % self.gitUser)
		if status != 200:
			return None

		allProjects = []

		for project in repos:
			allProjects.append(self._formatProject(project))

		return allProjects
