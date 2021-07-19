# crossword-web-app

## Structure folders
* app:
  > main process of application  
  > **src** folder is the path folder of application where ***src/main.py*** is the entry file
* docs: 
  - basic rules - βασικοί κανόνες
  - process structure - δομή κώδικα

## Setup Environment
It is better to run this application in a virual environment  

```python
  # python3
  # pip3 package-management system
  # virtual environment - virtualenv
  
  # Run server
  $ cd crossword_generator/
  $ source bin/activate #activate environment
  $ flask run

  $ deactivate #exit environment

  #install any package locally in virtual environment
  $ cd crossword_generator/
  $ python3 -m pip install -r requirements.txt

```

```javascript
  // Instalation
    // 1. needs npm/yarn package manager

  // Run vue app
  $ cd app/frontend/cross_app
  $ npm install / yarn install
  // see readme.md

```