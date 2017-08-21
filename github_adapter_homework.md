Your task is to implement a web-service which exposes some
of github.com's functionalities to its clients. The functionalities to
be exposed via a RESTful API are:

  a. given a github user, find all users which follows that person and
  return each of those followers: name, email, location and total
  number of repositories they own.  
    
    - https://developer.github.com/v3/users/#get-a-single-user
    - https://developer.github.com/v3/users/followers/#list-followers-of-a-user

  b. given a changeset and a repository, create a pull request 
  and at the same time request the reviews from the given users.
  
    - https://developer.github.com/v3/pulls/#create-a-pull-request
    - https://developer.github.com/v3/pulls/review_requests/#create-a-review-request

  c. allow a user to login to github (using their github's
  credentials) then, design and implement a way which will allow this
  user to make further requests to the web service to request data
  about their personal data, for example:

   - in case the user is logged in, the functionality required at
     subparagraph a. will return that user's followers details
  
  
Non-functional requirements:
  - use github's REST API V3 (https://developer.github.com/v3/)

  - **don't use** any github's client library (e.g. the ones listed
    here: https://developer.github.com/v3/libraries/)

  - use flask (https://pypi.python.org/pypi/Flask) as the web framework

  - provide tests with your project

  - please provide instructions how to run the project

  - use **strictly json** to expose the required functionalities (no html, css, js)

  - consider edge case such as users with a lot of followers
    (e.g. https://github.com/gvanrossum?tab=followers) and design an efficient solution.
    
# TODO:
 - unified gh response handler for catching errors and passing response otherwise
 - request for paginated queries ..
 - .. and paginated responses
 - request with auth
