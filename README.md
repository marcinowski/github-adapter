# Github adapter

## What is it?
This web application provides proxy API for some of the GitHub functionalities as well as a simple UI for explaining
the usage of API. Main functionalities are:
 - fetching data about logged in user or any other user from GitHub along with its followers
 - creating Pull Requests along with automatic reviewers assignment
 - basic user authentication simplifying above operations to selected user

## How to use API?
Let's explore the pure API side.

Github adapter API uses the following endpoints:
  - `/api` - full API documentation
  - `/api/login` - for user authentication
  - `/api/logout` - for logging out
  - `/api/user[?username=<username>]` - for user data fetching
  - `/api/pull_request` - for creating pull requests

All responses are returned in `json` format, some of them are paginated (see *pagination* section).
### Non authenticated user

Let's explore the functionalites for non authenticated users with `curl` command alongside with python `requests` library.
 
**Note** in examples below it's assumed that you run the app on `127.0.0.1:5000` or `localhost:5000`. Change the domain accordingly to your needs. 

Executing:
  
    curl http://127.0.0.1:5000/api/user?username=octocat
    or
    requests.get('http://127.0.0.1:5000/api/user?username=octocat
    
results in the following response:
    
    [
      {
        "name": "Test User",
        "location": "Sydney",
        "email": null,
        "public_repos": 12,
      },
      {
        "name": "Test User2",
        "location": "Sydney",
        "email": testuser2@test.com,
        "public_repos": 31,
      }
    ]
#### TODO: Pagination

For the pull request endpoint, executing:
    
    data = {
      'owner': 'test_user',
      'name': 'test_repository',
      'title': 'test_pull_request',
      'head': 'test_branch',
      'base': 'master',
      'reviewers': ['test_reviewer', 'test_reviewer_2'],
      'body': 'This pull request is a test',
    }
    curl -d $data http://127.0.0.1:5000/api/pull_request
    or
    requests.get('http://127.0.0.1:5000/api/pull_request', data=data)

results in:

    {
      "Status": "201 Created"
      "Location: https://api.github.com/repos/test_user/test_repository/pulls/1
    }
    
More specific documentation is included under `127.0.0.1:5000/api` endpoint.

### Authenticated user:
Methods described below simply assume default `username`, methods above with explicit `username` are still valid.
Let's explore authenticating the user using `Session` from python `request` library as we need a session object to keep the user
authenticated, `curl` wouldn't work here, unless keeping the session open.

To log in:

    from requests import Session
    s = Session()
    s.post('http://127.0.0.1:5000/api/login', data={'username': 'test', 'password': 'pwd'})
    
this returns:
    
    {
      "Status": "200 Authenticated"
    }

Now, using the same session object we can:
    
    s.get('http://127.0.0.1:5000/api/user')
    
which returns followers for authenticated user in the same format as above.

Similarly:

    s.post('http://127.0.0.1:5000/api/pull_request', data=data)
    
doesn't require providing `username` in data, as it's assumed.

To log out:
    
    s.get('http://127.0.0.1:5000/api/logout')

## How to use API with simple UI?

API has been wrapped with a simple UI forms for demonstrating purposes. Main endpoints are:
 - `/` - main page
 - `/login` - login page
 - `/pull_request` - pull request creation form
 - `/user` - user data fetching form

All above endpoints redirect to it's bound API endpoints returning pure `json` response.

## Technicalities

### Stack
Project uses `flask` framework along with `flask-RESTPlus` for API side. It's designed for GitHub REST API v3 
(https://developer.github.com/v3/). 

### Authentication
For authentication HTTPBasicAuth is used and after successful authentication 
credentials are stored inside `flask` session object and user is authenticated with each request. Flask session
object is not shared outside of the application. OAuth is not used
as it's a simple project to show designing simple API's and sharing the project would require generating individual OAuth 
tokens for each setup or sharing a private token which is certainly a bad idea. For a stand-alone usage of this project
OAuth could easily be implemented using `oauthlib` or `request-oauthlib` libraries.

## Project setup
System requirements: Python > 3 (not tested on 2.* versions)

To setup the project it's recommended to use virtualenv, but it can be skipped.
 1. `git clone https://github.com/marcinowski/github-adapter`
 2. (optional) `virtualenv venv && venv/bin/activate` (or `venv\Scripts\activate` on Windows)
 3. `pip install -r requirements.txt`
 4. `python src/app.py` # starts local server on port 5000 which is now accesible in your browser under `127.0.0.1:5000`
 
Alternatively you can use `setup.cmd` or `setup.sh` commands in the project root after fetching the repository.
(it's assumed that `python`, `pip` and `virtualenv` executables are added to your system path)

**Note** I don't have my Linux environment set up and I'm using Windows so Linux setup script isn't properly tested.
It should work when run from the directory it's located in.

## Tests
To run tests run `pytest`
