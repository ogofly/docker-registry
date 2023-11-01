import requests
from requests.auth import HTTPBasicAuth

# Docker Registry URL
registry_url = 'http://localhost:5080/v2/'

# Basic Auth credentials
username = 'test'
password = 'test'

# Get the list of repositories
response = requests.get(registry_url + '_catalog', auth=HTTPBasicAuth(username, password))
repos = response.json()['repositories']

# Iterate over each repository
for repo in repos:
    # Get the list of tags for the repository
    response = requests.get(registry_url + repo + '/tags/list', auth=HTTPBasicAuth(username, password))
    tags = response.json()['tags']
    print(f"repo {repo} tags: {tags}")
    if tags == None:
        continue

    # Sort the tags in descending order (assuming tags are in timestamp format)
    sorted_tags = sorted(tags, reverse=True)

    print('tags: repo: %s  %s' % (repo,sorted_tags))

    # Delete tags
    for tag in sorted_tags[:]:
        # TODO: keep some tags 
        delete_url = registry_url + repo + '/manifests/' + tag
        header = {"Accept": "application/vnd.docker.distribution.manifest.v2+json"}
        response = requests.head(delete_url, auth=HTTPBasicAuth(username, password), headers=header)
        if response.status_code != 200:
            print(f"{repo}:{tag} not exist, http status: {response.status_code}")
            continue
        digest = response.headers['Docker-Content-Digest']

        delete_url_with_digest =  registry_url + repo + '/manifests/' + digest
        print(delete_url_with_digest)
        response = requests.delete(delete_url_with_digest, auth=HTTPBasicAuth(username, password))

        if response.status_code == 202:
            print(f"Deleted image {repo}:{tag}")
        else:
            print(f"Failed to delete image {repo}:{tag}")
            print(f"response: {response.status_code}, {response.json()}")