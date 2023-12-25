# ------------------------------ IMPORTS ------------------------------ #

# modules to host server locally
from flask import Flask, request, Response, jsonify
from flask_cors import CORS # to allow cross-origin requests

# modules to interact with the API
import assets.scripts.api as Api

# json module to load strings to json
import json

# ------------------------------  SERVER SETUP ------------------------------ #

# initialize the flask app
app = Flask(__name__)

# allow cross-origin requests
CORS(app)

# ------------------------------  READING FROM CONFIG FILE ------------------------------ #

# read the config file
with open("assets/config.json", "r") as config_file:

    # load the config file and get the use_proxies variable to pass to the API
    use_proxies: bool = json.load(config_file)["use_proxies"]

# ------------------------------  API SETUP ------------------------------ #

# initialize the api
api = Api.Api(use_proxies=use_proxies)

# create a new session
api.create_new_session()

# ------------------------------  ROUTES ------------------------------ #

# this route handles chat completions
@app.route("/chat/completions", methods=["POST"])
def chat_completion():

    # get request data
    data = request.get_json()

    # get the messages
    messages = data["messages"]

    # check if messages has a system message
    if messages[0]["role"] == "system":

        # enable system messages in ai
        api.get_system_message(messages)

    # try applying the assistants first message
    try:

        api.apply_assistant_first(messages)

    except KeyError:

        # we can pass this one
        pass

    # this function handles streaming
    def stream():

        # generate a response
        response = api.chat(messages)

        # iterate through the response
        for chunk in response:

            # yield the response
            yield b'data: ' + str(chunk).encode() + b'\n\n'

        # finally, yield the last chunk
        yield b'data: [DONE]'

    # check if the user wants to stream
    if data["stream"]:

        # return a response
        return Response(
            stream(),
            mimetype="text/event-stream"
        )
    
    # otherwise, return a simple response
    else:

        # pre-define an empty full response
        full_response: str = ""

        # generate a response
        for chunk in api.chat(messages):

            # try to parse the chunk as json
            try:

                # append the chunk's contents to the full response
                full_response += json.loads(chunk)["choices"][0]["delta"]["content"]

            except KeyError:

                # we can pass this one. this means the stream is done.
                pass

        # return full response packed to a full non-streamed API response
        return Api.fill_response(full_response)


# route that returns the current model available for chat
@app.route("/models", methods=["GET"])
def get_model():

    """Route that returns the current model available for chat"""

    # return a response
    return jsonify(api.get_model()), 200

# route to handle the home page
@app.route("/")
def home():

    """Route to handle the home page"""

    # return a response. A simple HTML page which says that the reverse proxy is working as expected.
    return Response(
        response="<h2>Your generated link works! The reverse proxy is working as expected.</h2>",
        status=200,
        mimetype="text/html"
    )

# ------------------------------  END OF SETUP ------------------------------ #

# start the server
if __name__ == "__main__":

    # run the app
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )

# Path: app.py