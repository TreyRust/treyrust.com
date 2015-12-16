from flask import Flask, render_template, redirect
import projectpropagator, pagekit, mistune

app = Flask(__name__)

def getKit(base):
	navLinks = [('blog', 'Blog'),
				('demos', 'Tech Demos'),
				('projects', 'Projects'),
				('codingchallenges', "Trey's Coding Challenges")]

	cleanedNavLinks = []

	for top, title in navLinks:
		current = False
		if base == top:
			current = True

		cleanedNavLinks.append((top, title, current))

	return {'nav': cleanedNavLinks}

@app.route('/', methods=['GET'])
def root_get():
	return redirect('/blog/')

@app.route('/blog/', methods=['GET'])
def blog_get():
	return render_template('template.html', kit = getKit('blog'))

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



