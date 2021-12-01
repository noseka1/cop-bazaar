# COP Bazaar

The *cop_bazaar.py* script in this repository generates a static web site that collects information about COP git repositories.

Python 3 is required to run this script.

To generate a static web site issue:
```
$ TOKEN=<your_github_token> ./cop_bazaar.py
```

If you don't have a GitHub token, you can run without it as well, however, the script will fail due to rate limiting done by GitHub:

```
Exception: Failed to fetch data for repo https://github.com/RedHatOfficial/ocp4-helpernode. Response was: {   'documentation_url': 'https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting',
    'message': "API rate limit exceeded for 174.66.173.63. (But here's the "
               'good news: Authenticated requests get a higher rate limit. '
               'Check out the documentation for more details.)'}
```

The list of git repositories scraped is configured in *config.yaml*file.

COP Bazaar is used to generate [OpenShift Bazaar Source Code Index](https://github.com/noseka1/cop-bazaar/blob/output/output/README.md).
