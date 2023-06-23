from flask import Flask, render_template, request
from main import find_most_complex_repository

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        github_url = request.form['github-url']
        result = find_most_complex_repository(github_url)
        return render_template('index.html', result=result)
    else:
        return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run()
