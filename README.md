# crossword-web-app

## Preview
<img src="./assets/preview-app.gif" alt="">


## Description
This is a Automatic Crossword generator web application. Basically, speciallized on filling a theme crossword and follows all the basic known rules.


## Install
### Python
  ```python
    $ python3 -m pip install -r requirements.txt
  ```
### Javascript  
  Move terminal to cross_app folder
  ```python
    $ cd app/frontend/cross_app
  ```
  Install packages  
  ```javascript
    $ npm install 
  ```
  or with yarnpkg
  ```javascript
    $ yarn install
  ```




## Usage
1. Backend  
    Activate virtual environment
    ```python
      $ source bin/activate
    ```  
    Run server
    ```python
      $ flask run
    ```
    Exit environment  
    ```python
      $ deactivate
    ```
2. Frotend  
    Run vue app locally
    ```javascript
      $ npm run serve
    ```
    or with yarnpkg
    ```javascript
      $ yarn serve
    ```


## Docs
  Additionaly, you may have in mind read all the rules and other relative docs in the docs folder
  - basic rules - βασικοί κανόνες
  - process structure - δομή κώδικα


## Printing
> Present: .pdf

> Future: .puz, LateX


## Contributing
When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a code of conduct, please follow it in all your interactions with the project.

Contributions affect only the effort of generating the grid with words. After that all the PRs wil be ignored. The Last step certainly is the json translated in the API. Frontend is just for viewing.

Pull Request Process
1. Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2. Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent. The versioning scheme we use is SemVer.
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.
