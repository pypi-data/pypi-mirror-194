### **Setup**
poetry runs a venv, so you need to run `poetry install` from the root of the repo first

#### **Run**
`poetry run updater`

#### **Test**
`poetry run pytest` 

#### **Coverage**
`poetry run pytest --cov` or `poetry run pytest --cov --cov-report=term-missing`

### **Publish to PyPi**
After adding credentials to be able to push to the python package index run the following cmd:
`poetry publish --build`

##### **Linting**
Install nox with:
`pip3 install nox`
add the path to your .bashrc and source it

run `nox -rs black`
##### **Testing with console.py**

from within the src/scribe_updater/ directory run the following:
`poetry run updater --target ../tests/test_input_1.json --ground ../tests/test_ground_1.json --output ./test_output`
'
##### **PBA Customer Spreadsheet Updater (`update.py`)**
Injects new scenarios from the ground truth into a customer spreadsheet.
##### **Caveats**
if you are getting an error that looks like this :<br> `Failed to create the collection: Prompt dismissed..`<br>
then export the following environment variable: <br>
`export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring`

### **Usage**

basic use with no variables or mapping<br>
`updater -t target.json -g ground.json -o output.json`

use with variables (variables are only required when adding special products)<br>
`updater -t target.json -g ground.json -v variables.json -o output.json`

use with version map<br>
`updater -t target.json -g ground.json -m 3.3_to_3.7.json -o output.json`

use with variables & version maps<br>
`updater -t target.json -g ground.json -v variables -m 3.3_to_3.7.json -o output.json`


### **Version Mappings**

Version mappings are necessary when upgrading to a version that has scenarios that still exist but have been moved or their names have been changed. If you omit the version map the updater will still work but may delete or add scenarios that should not be in the configuration.

#### Available Mappings
<ol>
    <li>3.3_to_3.7.json (use this to upgrade to finie 3.8)</li>
    <li>3.3_to_3.6.json</li>
    <li>3.3_to_3.5.json (use this to upgrade to finie 3.8)</li>
</ol>