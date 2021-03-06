# Github adapter

## Table of contents:
 - What is it? [#](#base)
 - How to use API? [#](#api)
 - How to use API with simple UI? [#](#ui)
 - Technicalities [#](#tech)
 - Project Setup [#](#setup)
 - Tests [#](#tests)

## <a name="base"></a> What is it?
This web application provides proxy API for some of the GitHub functionalities as well as a simple UI for explaining
the usage of API. Main functionalities are:
 - fetching data about logged in user or any other user from GitHub along with its followers
 - creating Pull Requests along with automatic reviewers assignment
 - basic user authentication simplifying above operations to selected user

## <a name="api"></a> How to use API?
Let's explore the pure API side.

Github adapter API uses the following endpoints:
  - `/api` - full API documentation
  - `/api/login` - for user authentication
  - `/api/logout` - for logging out
  - `/api/user/followers[?username=<username>]` - for user's followers data fetching
  - `/api/user[?username=<username>]` - for user's data
  - `/api/pull_request` - for creating pull requests

All responses are returned in `json` format, some of them are paginated (see [pagination](#pagination)).
### Non authenticated user

Let's explore the functionalites for non authenticated users with `curl` command alongside with python `requests` library.
 
**Note** in examples below it's assumed that you run the app on `127.0.0.1:5000` or `localhost:5000`. Change the domain accordingly to your needs. 

#### User endpoints

Executing:
  
    curl http://127.0.0.1:5000/api/user/followers?username=octocat
    or
    requests.get('http://127.0.0.1:5000/api/user/followers?username=octocat
    
results in the following response:
    
    { 
      "first_url": <url/None>,
      "prev_url": <url/None>,
      "next_url": <url/None>,
      "last_url": <url/None>,
      "data: [
        {
          "name": "Test User",
          "location": "Sydney",
          "email": null,
          "public_repos": 12,
          "login": "testuser"
        },
        {
          "name": "Test User2",
          "location": "Sydney",
          "email": testuser2@test.com,
          "public_repos": 31,
          "login": "testuser"
        }
      ]
    }

#### <a name="pagination"></a> Pagination
Above response is an example of a paginated response. Note the `first/prev/next/last` urls,
they're responsible for paginated continuity of API. Depending on API endpoint
you can manipulate page size by `?per_page=...` parameter (for `/followers` 10 is forced, because of a long waiting time
for the resource, please see the implementation in src.api.users.py:FollowerResource)

#### User data
Endpoint for fetching user data (name, location, email)

    curl http://127.0.0.1:5000/api/user?username=octocat
    or
    requests.get('http://127.0.0.1:5000/api/user?username=octocat

Response:

    {
      "data": {
        "name": "Test User",
        "location": "Sydney",
        "email": null,
        "public_repos": 12,
        "login": octocat
        ...
      }
    }

#### Pull request
For the pull request endpoint, executing:
    
    data = {
      'owner': 'test_user',
      'name': 'test_repository',
      'title': 'test_pull_request',
      'head': 'test_branch',
      'base': 'master',
      'reviewers': 'test_reviewer,test_reviewer_2',
      'body': 'This pull request is a test',
    }
    
    curl -d $data http://127.0.0.1:5000/api/pull_request
    or
    requests.get('http://127.0.0.1:5000/api/pull_request', data=data)

results in:

    {
      "data": {
        ... GitHubResponse .. 
      }
    }
    
where GitHubResponse [as here](https://developer.github.com/v3/pulls/review_requests/#response)

More specific documentation is included under `127.0.0.1:5000/api` endpoint and in code docs.

### Authenticated user:
Methods described below simply assume default `username`, methods above with explicit `username` are still valid.
Let's explore authenticating the user using `Session` from python `request` library as we need a session object to
keep the user authenticated, `curl` wouldn't work here, unless keeping the session open. 
Browsing this API also ensures keeping the session.

To log in:

    from requests import Session
    s = Session()
    s.post('http://127.0.0.1:5000/api/login', data={'username': 'test', 'password': 'pwd'})
    
this returns:
    
    {
      "data": {
        ...GitHubUserData...
      }
    }

where GitHubUserData [as here](https://developer.github.com/v3/users/#response)

#### Users endpoint

Now, using the same session object we can:
    
    s.get('http://127.0.0.1:5000/api/user/followers')
    
which returns followers for authenticated user in the same format as above.

#### Pull request

Similarly:

    s.post('http://127.0.0.1:5000/api/pull_request', data=data)
    
doesn't require providing `username` in data, as it's assumed (however you can still 'overwrite' that parameter).

To log out:
    
    s.get('http://127.0.0.1:5000/api/logout')

### Error handling
Errors in json format come in format:

    {
      "detail_reason": "Not Found",
      "reason": "Page not found",
      "status_code": 404
    }

`detail_reason` shows an error message from GitHub API, `reason` shows GitHub Adapter error message.
Sometimes one of them is more detailed, which can indicate where has the error occured.

## <a name="ui"></a> How to use API with simple UI?

API has been wrapped with a simple UI forms for demonstrating purposes. Main endpoints are:
 - `/` - main page
 - `/login` - login page
 - `/logout` - log out endpoint 
 - `/pull_request` - pull request creation form
 - `/user` - user data fetching form
 - `/followers` - user followers data fetching form

If you're authenticated, most forms will automatically fill out your name, which naturally you can change.
All above endpoints redirect to it's bound API endpoints returning pure `json` response.

## <a name="tech"></a> Technicalities

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

### Highlights
 - exception/response handling with `catch_http_error` decorator
 - paginated followers response
 - definitely logo

## <a name="setup"></a> Project setup
System requirements: Python > 3 (not tested on 2.* versions).
If you work in a closed internal network, make sure you set `http_proxy` & `https_proxy` in environment variables.

To setup the project it's recommended to use virtualenv, but it can be skipped.
 1. `git clone https://github.com/marcinowski/github-adapter`
 2. (optional) `virtualenv venv && venv/bin/activate` (or `venv\Scripts\activate` on Windows)
 3. `pip install -r requirements.txt`
 4. `python src/app.py` # starts local server on port 5000 which is now accesible in your browser under `127.0.0.1:5000`
 
Alternatively you can use `setup.cmd` or `setup.sh` commands in the project root after fetching the repository.
(scripts assume that `python`, `pip` and `virtualenv` executables are added to your system path) Scripts can take about 
couple of minutes (3 minutes max I guess), depending on your internet connection and hardware.

**Note** I don't have my Linux environment set up and I'm using Windows so Linux setup script isn't properly tested.
It should work when run from the directory it's located in.

## <a name="tests"></a> Tests

There are over 40 tests written in this project. To be fair, they need more time to develop (not very DRY, not too many,
lack of verbose unit/functional separation). 

To run the tests activate `virtualenv` if you use one and run `pytest` from project root directory.

To check PEP8 run `pytest --pep8`.

To test API manually you can do for example:

**Testing session authentication:**
 1. `/api/user` - 400 Bad Request
 2. `/login` - pass your credentials with neat form
 3. `/api/user` - 200 OK - user authenticated
 4. `/api/logout` - Logging out
 5. `/api/user` - 400 Bad Request
