# CodeMonsters Sanity Check App

### Description
This app could be used to test the CodeMonsters API. It is a command line tool which takes a config file as input and 
runs sanity checks using it. If no config is provided as an argument, the default one is used instead. Please refer to 
the builtin help for more usage info.

### Config
The config file needs to be a valid json file with the following keys: "credentials", "endpoints", "test_data", 
"expected_responses". You can use the included config file for reference.

### Setup
The project uses Python 3. For installing the requirements, you need to have ``pip`` installed.
Go to the project's root folder and run `pip install -r requirements.txt`.

### Sanity suite
To run the sanity suite, execute `python3 app.py -s`. The suite itself could be easily extended with new request 
issuing functions and cases.

### Tests
To run the unit tests, simply execute `tox` in the root folder.
