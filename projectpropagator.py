import requests

class GitHubPropagator:
	def __init__(self, userAgent, gitUser):
		self.userAgent = userAgent
		self.gitUser = gitUser

	def _getRequest(self, url):
		resp = requests.get(url, headers = {"User-agent": self.userAgent})
		return resp.json(), resp.status_code

	def _formatProject(self, project):
		return {"name": project['name'], "lastUpdated": project['updated_at'],
				"created": project['created_at'], "forkCount": project['forks']}

	def getProject(self, name):
		url = "https://api.github.com/repos/%s/%s" % (self.gitUser, name)
		repo, status = self._getRequest(url)

		return self._formatProject(repo)

	def getAllProjects(self):
		repos, status = self._getRequest("https://api.github.com/users/%s/repos" % self.gitUser)

		allProjects = []

		for project in repos:
			allProjects.append(self._formatProject(project))

		return allProjects

myProp = GitHubPropagator("Project Propagator for treyrust.com", "TreyRust")
print myProp.getAllProjects()