# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['helper_auth']

package_data = \
{'': ['*']}

extras_require = \
{'requests': ['requests>=2,<3']}

setup_kwargs = {
    'name': 'helper-auth',
    'version': '0.6.0',
    'description': 'Request authentication using existing credential helpers.',
    'long_description': '[![helper-auth on PyPI][PyPI badge]][PyPI page]\n\nThis Python library provides the `HelperAuth` class whose objects are intended\nto be used as custom authentication handlers in conjunction with\nthe [Requests] library, as suggested in its [documentation].\n\n\n# Installation\n\n```\npip install helper-auth\n```\n\nPlease note that while `helper-auth` is supposed to be used in\nenvironments with `requests` installed, it does not depend on it.\nTo install `requests` together with `helper-auth`, specify it as an extra:\n\n```\npip install \'helper-auth[requests]\'\n```\n\n\n# Usage\n\nSuppose you have an existing GitHub personal access token, and\na [Git credential helper] already set up for Git to authenticate to\nGitHub using this token as the password. This helper prints the following\nto standard output:\n\n```\n$ git credential-github\nusername=YOUR_GITHUB_USERNAME\npassword=YOUR_GITHUB_TOKEN\n```\n\nYou want to use the same token to make GitHub API calls using the Requests\nlibrary. The API expects a `token YOUR_GITHUB_TOKEN` string as the value of\nyour request\'s `Authorization` header.\n\nYou can use `HelperAuth` with its default settings:\n\n```python\nimport requests\nfrom helper_auth import HelperAuth\n\nauth = HelperAuth("git credential-github")\n\nresponse = requests.get("https://api.github.com/user", auth=auth)\n```\n\n\n## Specifying the helper command\n\nThe helper command can be specified as one or more positional arguments:\n\n```python\nauth = HelperAuth("helper")\n```\n\n```python\nauth = HelperAuth("helper", "--option", "arg")\n```\n\nAs a shortcut, a command with command-line arguments can also be passed\nas a single string:\n\n```python\nauth = HelperAuth("helper --option arg")\n```\n\nIn addition, the first positional argument can be a path-like object:\n\n```python\nauth = HelperAuth(Path("helper"))\n```\n\n```python\nauth = HelperAuth(Path("helper"), "--option", "arg")\n```\n\n\n## Caching the token\n\nBy default, a `HelperAuth` object never stores the value of the token\n(password) in its internal state. Rather, the helper command is invoked\neach time the object is called. This is an intentional precaution (such\nthat the token cannot be retrieved *ex post* by the introspection of the\n`HelperAuth` object) but it can also be unnecessarily expensive if the object\nis to be called repeatedly, e.g. when making many simultaneous API calls.\nYou can override this behavior by passing `cache_token=True` to the\nconstructor:\n\n```python\nauth = HelperAuth("helper", cache_token=True)\n```\n\nThe cached token can then be cleared anytime by calling\n\n```python\nauth.clear_cache()\n```\n\n[PyPI badge]: https://img.shields.io/pypi/v/helper-auth\n[PyPI page]: https://pypi.org/project/helper-auth\n[Requests]: https://requests.readthedocs.io\n[documentation]: https://requests.readthedocs.io/en/latest/user/authentication/#new-forms-of-authentication\n[Git credential helper]: https://git-scm.com/docs/gitcredentials#_custom_helpers\n',
    'author': 'Michal Porteš',
    'author_email': 'michalportes1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mportesdev/helper-auth',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
