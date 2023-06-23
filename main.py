# Modify the function to return the result as a dictionary
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
        result = {
            'name': most_complex_repo['name'],
            'url': most_complex_repo['html_url'],
            'analysis': f"The complexity score is: {highest_complexity_score}"
        }
        return result
    else:
        return None
