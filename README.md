# Kicstarter Success API

This provides a micro-service backend for the Kickstarter Success project at Lambda School,
August 2020. It accepts as inputs JSON data containing attributes of a proposed crowd funded
project on Kickstarter, and returns a prediction of the project success or failure to be
funded. This implements a neural netowrk based on data on previous projects on Kickstarter,
including their final outcomes.

It is actively deployed on Heroku, https://kickstarter-dspt6-project.herokuapp.com/.

The data is received in the form of a json (as an HTML POST) that has the following keys
with associated values:

name: str. The name of the Project

desc: str. A description of the project

goal: float. The goal (amount of money) required for the project

disable_communication: bool. Whether the project authors has disabled communication 
option with people donating to the project

country: str. The country of the project's author

currency: str. The currency in which the goal (amount) is required

campaign_length: The length of the campaign measured in days

If succesful, the model then returns a JSON containing output of [1,0] that is returned
to the Kickstarter Success App to be displayed to the user. If the input is incomplete,
the API returns a response code of 400 (bad request) and an error message; if an exception
occurs, it returns a response code of 500 (internal error) and an error message.

This API is not intended for public use, but is designed as a backend service for the
associated Kickstarter Success application. However, it does not require authentication. It
is stateless (and thus RESTful).

The /test_api also provides a UI to try out the service. It was primarily intended for the
dev team for testing purposes.