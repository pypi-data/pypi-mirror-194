# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scribe_updater']

package_data = \
{'': ['*'], 'scribe_updater': ['version_mapping/*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'nox>=2022.11.21,<2023.0.0']

entry_points = \
{'console_scripts': ['updater = scribe_updater.console:main']}

setup_kwargs = {
    'name': 'scribe-updater',
    'version': '0.17.2',
    'description': 'A tool to upgrade scribe configuration files',
    'long_description': "### **Setup**\npoetry runs a venv, so you need to run `poetry install` from the root of the repo first\n\n#### **Run**\n`poetry run updater`\n\n#### **Test**\n`poetry run pytest` \n\n#### **Coverage**\n`poetry run pytest --cov` or `poetry run pytest --cov --cov-report=term-missing`\n\n### **Publish to PyPi**\nAfter adding credentials to be able to push to the python package index run the following cmd:\n`poetry publish --build`\n\n##### **Linting**\nInstall nox with:\n`pip3 install nox`\nadd the path to your .bashrc and source it\n\nrun `nox -rs black`\n##### **Testing with console.py**\n\nfrom within the src/scribe_updater/ directory run the following:\n`poetry run updater --target ../tests/test_input_1.json --ground ../tests/test_ground_1.json --output ./test_output`\n'\n##### **PBA Customer Spreadsheet Updater (`update.py`)**\nInjects new scenarios from the ground truth into a customer spreadsheet.\n##### **Caveats**\nif you are getting an error that looks like this :<br> `Failed to create the collection: Prompt dismissed..`<br>\nthen export the following environment variable: <br>\n`export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring`\n\n### **Usage**\n\nbasic use with no variables or mapping<br>\n`updater -t target.json -g ground.json -o output.json`\n\nuse with variables (variables are only required when adding special products)<br>\n`updater -t target.json -g ground.json -v variables.json -o output.json`\n\nuse with version map<br>\n`updater -t target.json -g ground.json -m 3.3_to_3.7.json -o output.json`\n\nuse with variables & version maps<br>\n`updater -t target.json -g ground.json -v variables -m 3.3_to_3.7.json -o output.json`\n\n\n### **Version Mappings**\n\nVersion mappings are necessary when upgrading to a version that has scenarios that still exist but have been moved or their names have been changed. If you omit the version map the updater will still work but may delete or add scenarios that should not be in the configuration.\n\n#### Available Mappings\n<ol>\n    <li>3.3_to_3.7.json (use this to upgrade to finie 3.8)</li>\n    <li>3.3_to_3.6.json</li>\n    <li>3.3_to_3.5.json (use this to upgrade to finie 3.8)</li>\n</ol>",
    'author': 'Paul Cardoos',
    'author_email': 'paul.cardoos@clinc.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
