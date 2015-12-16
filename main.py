from flask import Flask, render_template
import projectpropagator

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root_get():
	return render_template('template.html')

@app.route('/projects/<projectName>', methods=['GET'])
def projects_name_get(projectName):
	myProp = projectpropagator.GitHubPropagator("Project Propagator for treyrust.com", "TreyRust")
	project = myProp.getProject(projectName)
	if not project:
		return render_template("projectpage.html", failedLoad = True)

	return render_template("projectpage.html", project = project)


@app.route('/projects/', methods=['GET'])
def projects_get():
	myProp = projectpropagator.GitHubPropagator("Project Propagator for treyrust.com", "TreyRust")
	allProjects = myProp.getAllProjects()
	if not allProjects:
		return render_template('projects.html', failedLoad = True)

	return render_template('projects.html', allProjects = allProjects)

if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0')



