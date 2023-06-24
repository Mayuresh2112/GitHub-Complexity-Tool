from flask import Flask, render_template, request
import requests
import os
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        github_url = request.form['github_url']
        repositories = fetch_user_repositories(github_url)

        if repositories:
            most_complex_repository = find_most_complex_repository(repositories)
            complexity_justification = gpt_justification(most_complex_repository)
            analysis = perform_gpt_analysis(most_complex_repository)  # Perform GPT-based analysis
            return render_template('result.html', repo_url=most_complex_repository["html_url"], analysis=analysis)
        else:
            return render_template('index.html', result=False)
    return render_template('index.html', result=None)



def fetch_user_repositories(github_url):
    # Extract username from GitHub URL
    username = github_url.split("/")[-1]

    # Send request to GitHub API to fetch user repositories
    api_url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(api_url)

    if response.status_code == 200:
        repositories = response.json()
        return repositories
    else:
        print("Failed to fetch user repositories.")
        return []

def preprocess_code(repository):
    # Clone the repository locally
    subprocess.call(["git", "clone", repository["clone_url"]])

    # Perform memory management and preprocessing on the code files
    repo_name = repository["name"]
    repo_path = os.path.join(os.getcwd(), repo_name)

    # Add your memory management and preprocessing techniques here

    # Example: Print the names of all Python files in the repository
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                print(os.path.join(root, file))

def evaluate_technical_complexity(code):
    # Implement your prompt engineering techniques and GPT evaluation here
    # Example: Return a random complexity score for demonstration purposes
    return 0.75

def find_most_complex_repository(repositories):
    most_complex_repo = None
    highest_complexity_score = 0

    for repository in repositories:
        preprocess_code(repository)
        complexity_score = evaluate_technical_complexity(repository["name"])

        if complexity_score > highest_complexity_score:
            highest_complexity_score = complexity_score
            most_complex_repo = repository

    return most_complex_repo

def gpt_justification(repository):
    # Implement GPT-based justification for the selection of the repository here
    # Example: Return a placeholder justification string for demonstration purposes
    return "The selected repository contains advanced algorithms and extensive usage of machine learning techniques, making it highly complex."

def perform_gpt_analysis(repository):
    # Implement GPT-based analysis logic here
    # Example: Return a placeholder analysis string for demonstration purposes
    return "The selected repository demonstrates a high level of technical complexity with intricate algorithm design and extensive use of advanced data structures."

if __name__ == '__main__':
    app.run(debug=True)

