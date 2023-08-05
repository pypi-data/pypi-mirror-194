# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aerostat',
 'aerostat.aws',
 'aerostat.core',
 'aerostat.static.python.lib.python3.9.site-packages.attachment_server',
 'aerostat.static.python.lib.python3.9.site-packages.attachment_server.excel']

package_data = \
{'': ['*'], 'aerostat': ['static/*']}

install_requires = \
['jinja2>=3.1.2,<4.0.0',
 'questionary>=1.10.0,<2.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['aerostat = aerostat.cli:app']}

setup_kwargs = {
    'name': 'aerostat-launcher',
    'version': '0.0.8',
    'description': 'A simple CLI tool to deploy your Machine Learning models to cloud, with public API and connection templates ready to go.',
    'long_description': '# Aerostat\n\nA simple CLI tool to deploy your Machine Learning models to cloud, with public API and template connections ready to go.\n\n## Get started\n### Installation\nThe name `Aerostat` has been used by another PyPI project, please install this package with:\n```bash\npip install aerostat-launcher\n```\nOnce installed, it can be used directly via `aerostat`. If it doesn\'t work, add `python -m` prefix to all commands,\ni.e. `python -m aerostat deploy`.\n\nOnly three commands needed for deploying your model: `install`, `login`, and `deploy`.\n\n### Setup\n1. Run the following command to install all the dependencies needed to run Aerostat. Please allow installation in the pop-up windows to\n   continue.\n```bash\naerostat install\n```\n\n2. To login to Aerostat, you need to run the following command:\n```bash\naerostat login\n```\nYou will be prompted to choose an existing AWS credentials, or enter a new one. The AWS account used needs to have **AdministratorAccess**.\n\n### Deploy\nTo deploy your model, you need to dump your model to a file with pickle, and run the following command:\n```bash\naerostat deploy\n```\nYou will be prompted to enter:\n- the path to your model file\n- the input columns of your model\n- the ML library used for your model\n- the name of your project\n\nOr you can provide these information as command line options like:\n```bash\naerostat deploy --model-path /path/to/model --input-columns "[\'col1\',\'col2\',\'col3\']" --python-dependencies scikit-learn --project-name my-project\n```\n\n## Connections\nAerostat provides connection templates to use your model in various applications once it is deployed. Currently, it includes templates for:\n- Microsoft Excel\n- Google Sheets\n- Python / Jupyter Notebook\n\nVisit the URL produced by the `aerostat deploy` command to test your model on cloud, and get the connection templates.\n\n## Other Commands\n### List\nTo list all the projects you have deployed, run:\n```bash\naerostat ls\n```\n\n### Info\nTo find deployment information of a specific project, such as API endpoint, run:\n```bash\naerostat info\n```\nthen choose the project from the list. You can also provide the project name as a command line option like:\n```bash\naerostat info my-project\n```\n\n## Future Roadmap\n- Improve user interface, including rewrite prompts with Rich, use more colors and emojis\n- Add unit tests\n- Adopt [Semantic Versioning](https://semver.org) once reach v0.1.0 and add\n  CI/[CD](https://mestrak.com/blog/semantic-release-with-python-poetry-github-actions-20nn)\n- Support SSO login\n- Support deploying to GCP',
    'author': 'Vincent Yan',
    'author_email': 'vincent.yan@blend360.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vinceyyy/Aerostat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
