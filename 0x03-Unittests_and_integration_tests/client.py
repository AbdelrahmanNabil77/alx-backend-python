import requests

def get_json(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

class GithubOrgClient:
    def __init__(self, org_name):
        self.org_name = org_name

    def org(self):
        """This is a method that returns the organization data."""
        return get_json(f"https://api.github.com/orgs/{self.org_name}")

    @property
    def _public_repos_url(self):
        """Returns the 'repos_url' from the org data"""
        return self.org().get("repos_url")

    def public_repos(self, license_key=None):
        """Returns list of public repository names, optionally filtered by license."""
        repos = get_json(self._public_repos_url)
        if license_key is None:
            return [repo["name"] for repo in repos]
        return [
            repo["name"] for repo in repos
            if self.has_license(repo, license_key)
        ]

    def has_license(self, repo, license_key):
        """Check if repo has the given license key."""
        return repo.get("license", {}).get("key") == license_key

