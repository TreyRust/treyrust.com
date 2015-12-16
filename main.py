from flask import Flask, render_template
import projectpropagator

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root_get():
	return render_template('template.html')

@app.route('/projects/', methods=['GET'])
def projects_get():
	myProp = projectpropagator.GitHubPropagator("Project Propagator for treyrust.com", "TreyRust")
	return render_template('projects.html', allProjects = myProp.getAllProjects())

if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0')



