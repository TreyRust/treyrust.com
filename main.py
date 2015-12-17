from flask import Flask, render_template, redirect
import projectpropagator, tumblrpropagator, mistune

app = Flask(__name__)

def getKit(base):
	navLinks = [('blog', 'Blog'),
				('projects', 'Projects'),
				('postmortems', 'Project Postmortems'),
				('codingchallenges', "Trey's Coding Challenges")]

	cleanedNavLinks = []

	for top, title in navLinks:
		current = False
		if base == top:
			current = True

		cleanedNavLinks.append((top, title, current))

	return {'nav': cleanedNavLinks, 'baseUrl': base}


def blogHelper(page, tag, startPos = 0, currentPage = 1):
	tumProp = tumblrpropagator.tumblrPropagator('treyrust', tag)
	posts, hasMore = tumProp.getPosts(startPos)

	if not posts:
		return render_template('blogroll.html', kit = getKit(page), failedLoad = True)

	return render_template('blogroll.html', kit = getKit(page),
											posts = posts,
											hasMore = hasMore,
											currentPage = currentPage,
											pagination = True)


@app.route('/', methods=['GET'])
def root_get():
	return redirect('/blog/')


@app.route('/blog/', methods=['GET'])
@app.route('/blog/page/<num>', methods=['GET'])
def blog_get(page = None, num = None):
	currentPage = 1
	startPos = 0
	if num:
		pageNum = 1
		try:
			pageNum = int(num)
		except: #this way, if we didn't get an int, it just defaults to 0 anyway
			pass

		if pageNum > 1:
			currentPage = pageNum
			startPos = (pageNum - 1) * 10 #Ten results per page.

	return blogHelper('blog', 'treyrust.com', startPos, currentPage)


@app.route('/postmortems/', methods=['GET'])
def postmortems_get():
	return blogHelper('postmortems', 'project postmortems')


@app.route('/codingchallenges/', methods=['GET'])
def codingchallenges_get():
	return blogHelper('codingchallenges', "trey's coding challenges")


@app.route('/projects/<projectName>', methods=['GET'])
def projects_name_get(projectName):
	myProp = projectpropagator.GitHubPropagator("Project Propagator for treyrust.com", "TreyRust")
	project = myProp.getProject(projectName)
	if not project:
		return render_template("projectpage.html", failedLoad = True)

	readme = myProp.getReadme(projectName)
	mdown = mistune.Markdown()
	readme = mdown(readme)

	return render_template("projectpage.html", kit = getKit('projects'), 
							project = project, readme = readme)


@app.route('/projects/', methods=['GET'])
def projects_get():
	myProp = projectpropagator.GitHubPropagator("Project Propagator for treyrust.com", "TreyRust")
	allProjects = myProp.getAllProjects()
	if not allProjects:
		return render_template('projects.html', failedLoad = True)

	return render_template('projects.html', kit = getKit('projects'), allProjects = allProjects)


if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0')



