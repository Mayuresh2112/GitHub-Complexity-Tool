# Modify the function to return the result as a dictionary
def find_most_complex_repository(github_url):
    repos = fetch_user_repos(github_url)
    if most_complex_repo:
        result = {
            'name': most_complex_repo['name'],
            'url': most_complex_repo['html_url'],
            'analysis': f"The complexity score is: {highest_complexity_score}"
        }
        return result
    else:
        return None
