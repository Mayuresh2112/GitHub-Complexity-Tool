from flask import Flask, render_template, request
import os
import re
import shutil
import requests
import git
import openai

# Set up OpenAI API credentials
openai.api_key = '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'

# Set up Flask app
app = Flask(__name__)

# Function to fetch user repositories from GitHub API
def fetch_user_repos(github_url):
    username = extract_username(github_url)
    api_url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(api_url)
    if response.status_code == 200:
        repos = response.json()
        return repos
    else:
        print(f"Failed to fetch repositories. Error: {response.text}")
        return []
    # Same code as before

# Helper function to extract username from GitHub URL
def extract_username(github_url):
    pattern = r'https://github.com/([^/]*)'
    match = re.match(pattern, github_url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid GitHub URL format")
    # Same code as before

# Function to clone a repository using GitPython
def clone_repository(repo_url, destination):
    git.Repo.clone_from(repo_url, destination)
    # Same code as before

# Function to preprocess code before passing it to GPT
def preprocess_code(code):
    processed_code = code  # Placeholder, modify as needed
    return processed_code
    # Same code as before

# Function to assess technical complexity using GPT
def assess_complexity(code):
    complexity_score = 0.5  # Placeholder, modify as needed
    return complexity_score
    # Same code as before

# Function to remove a directory and its contents
def remove_directory(directory):
    shutil.rmtree(directory)
    # Same code as before

# Placeholder function to get repository files
def get_repository_files(repository_path):
    files = []  # Placeholder, modify as needed
    return files
    # Same code as before

# Placeholder function to combine files content
def combine_files_content(files):
    combined_content = ''  # Placeholder, modify as needed
    return combined_content
    # Same code as before

# Main function to find the most complex repository
def find_most_complex_repository(github_url):
    repos = fetch_user_repos(github_url)

    if not repos:
        print("No repositories found.")
        return

    most_complex_repo = None
    highest_complexity_score = 0

    for repo in repos:
        repo_url = repo['html_url']
        repo_name = repo['name']
        clone_path = f"temp/{repo_name}"

        try:
            clone_repository(repo_url, clone_path)
            files = get_repository_files(clone_path)
            code = combine_files_content(files)
            preprocessed_code = preprocess_code(code)
            complexity_score = assess_complexity(preprocessed_code)

            if complexity_score > highest_complexity_score:
                highest_complexity_score = complexity_score
                most_complex_repo = repo

        except Exception as e:
            print(f"Error processing repository: {repo_name}")
            print(f"Error details: {str(e)}")

        finally:
            # Clean up cloned repository
            if os.path.exists(clone_path):
                remove_directory(clone_path)
                
    if most_complex_repo:
        print(f"The most complex repository is: {most_complex_repo['name']}")
        print(f"Complexity score: {highest_complexity_score}")
        print(f"Repository URL: {most_complex_repo['html_url']}")
    else:
        print("No complex repository found.")

    # Same code as before

# Flask route for the homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        github_url = request.form['github-url']
        result = find_most_complex_repository(github_url)
        return render_template('index.html', result=result)
    else:
        return render_template('index.html', result=None)

# Run the Flask app
if __name__ == '__main__':
    app.run()
