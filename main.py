from flask import Flask, render_template

app = Flask(__name__)

if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0')



@app.route('/', methods = ['GET'])
def root_get():
	return render_template('template.html')