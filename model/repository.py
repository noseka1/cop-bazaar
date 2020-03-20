import logging
import pprint
import requests

GITHUB_REPO_PREFIX = 'https://github.com/'
GITHUB_API = 'https://api.github.com/repos/'

class Repository(object):

    all = []

    def __init__(self, url, categories):
        self.url = url
        self.categories = categories
        self.data = dict()
        self.all.append(self)

    def fetchRepoData(self):

        logging.info("Fetching data for repo %s", self.url)

        if self.url.startswith(GITHUB_REPO_PREFIX):
            repo_path = self.url[len(GITHUB_REPO_PREFIX):]
            repo_info = requests.get('%s%s' % (GITHUB_API, repo_path))
            repo_json = repo_info.json()

            #pp = pprint.PrettyPrinter(indent=4)
            #pp.pprint(repo_json)

            self.data['repo_path'] = repo_path
            self.data['description'] = repo_json['description']
            self.data['html_url'] = repo_json['html_url']
            self.data['pushed_at'] = repo_json['pushed_at']
            self.data['stargazers_count'] = repo_json['stargazers_count']
            self.data['forks_count'] = repo_json['forks_count']
