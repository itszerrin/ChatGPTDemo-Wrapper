# ------------------------------ IMPORTS ------------------------------ #

# for type hints
from ..typing import Headers, Chunk, Id, Messages, Any

# this module allows us to get default headers for all requests
from .headers.default_headers import get_default_headers

# to make HTTP requests
import requests

# fake useragent module to generate random user agents
import fake_useragent

# secrets module for safe generation of random numbers and strings
import secrets

# string module to assist in generating random strings
import string

# json module
import json

# logging module for debugging
import logging

# for free proxies (to not get blocked)
from fp.fp import FreeProxy
from fp.errors import FreeProxyException # to catch the error of no proxies being available

# ------------------------------  LOGGER SETUP ------------------------------ #

# create a logger
logger = logging.getLogger(__name__)

# set the logging level
logger.setLevel(logging.DEBUG)

# create a basic format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# ------------------------------  ADDITIONAL VARIABLES ------------------------------ #

# below is the first half of a dict which is supposed to contain a full OpenAI-type stream response
first_half_of_response = {

    "object": "chat.completion.chunk",
    "model": "gpt-3.5-turbo",
}

# ------------------------------  ADDITIONAL METHODS ------------------------------ #

# this method converts a list of messages to a string. Format: "role: content + \n"
def messages_to_str(messages: list[str, str]) -> str:

    """Converts a list of messages to a string"""

    # the string to be returned
    string: str = ""

    # iterate through the messages
    for message in messages:

        # append the message to the string
        string += f'{message["role"]}: {message["content"]}\n'

    # return the accumulated messages
    return string

# this method takes a message's content and fills it into a full non-streamed API response
def fill_response(message_content: str) -> dict[str, Any]:

    """Takes a message's content and fills it into a full non-streamed API response"""

    # the response to be returned
    non_streamed_response: dict[str, ] = json.dumps({
        "object": "chat.completion",
        "model": "gpt-3.5-turbo-0613",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": f"{message_content}",
            },
            "finish_reason": "stop",
        }],
    })

    # return the response
    return non_streamed_response

# ------------------------------  MAIN API CLASS ------------------------------ #

# main api class
class Api(object):

    # constructor
    def __init__(self, use_proxies: bool) -> None:

        """Constructor"""

        # the headers to be sent with the requests
        self.headers: Headers | dict[str, str] = get_default_headers(
            fake_useragent.UserAgent().firefox,
            secrets.randbelow(100)
        )

        # the url where the requests will be sent
        self.url: str = "https://chat.chatgptdemo.net"

        # the user id
        self.user_id: Id | str = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(17))

        # debug
        logger.info("User id: %s\n", self.user_id)

        # the session id - pre-initialized to an empty string
        self.session_id: str = ""

        # if the user wants to use proxies
        if use_proxies:

            logger.info("Creating a new proxy...\n") # debug

            # try statement because the proxies might not be available
            try:

                # create a new proxy list
                self.proxies = {
                        "http": FreeProxy(rand=True).get(),
                        "https": FreeProxy(rand=True, https=True).get(),
                }
                            
                logger.info("Proxy created. Proxy: %s\n", self.proxies["http"]) # debug

            # if the proxies are not available, catch the exception
            except FreeProxyException:

                # if the proxies are not available, use no proxies
                self.proxies = {}

                # debug
                logging.warning("No proxies available. Using no proxies.\n")

        # if the user does not want to use proxies
        else:

            # use no proxies
            self.proxies = {}

    # create a new session
    def create_new_session(self) -> None:

        """Create a new session"""

        # prepare the payload to be sent with the request
        payload: dict = {

            "user_id": self.user_id
        }

        # send the request and get the response
        self.session_id: str = requests.post(f"{self.url}/new_chat", json=payload, headers=self.headers, proxies=self.proxies).json()['id_'] # type string

        # debug
        logger.info("New session created. Session id: %s\n", self.session_id)

    # this function returns the current model available for chat
    def get_model(self) -> dict[str, list[str, str]]:

        """This function returns the current model available for chat"""

        return {"data": [
            {"id": "gpt-3.5-turbo-0613"} # can't be changed
        ]}

    # chat with the bot. Streams the response.
    def chat(self, messages_list: Messages) -> Chunk | dict[str, str]:
        
        """Chat with the bot. Streams the response."""

        # keep track using a log
        logger.info("Request sent to gpt-3.5-turbo. Message sent: %s\n", messages_list[-1]["content"])

        # prepare the payload to be sent with the request
        payload: dict = {

            "chat_id": f"{self.session_id}",
            "question": f"{messages_to_str(messages_list)}",
            "timestamp": f"{1}",

        }

        # create a session
        with requests.Session() as s:

            # update session proxies
            s.proxies.update(self.proxies)
            
            # send the request and get the response
            response = s.post(f"{self.url}/chat_api_stream", json=payload, headers=self.headers)

        # raise an exception if the status code is not 200
        response.raise_for_status()

        # the response data
        response_data: str = ""

        # iterate, one chunk at a time
        for chunk in response.iter_lines():
                
            # decode the chunk and remove the "data: " prefix and strip the trailing whitespace
            delta_chunk = chunk.decode('utf-8').replace("data: ", "").strip()

            # accumulate the chunks until a complete JSON object is obtained
            response_data += delta_chunk

            # check if the accumulated data is a complete JSON object
            if response_data.endswith("}"):

                try:

                    # convert the accumulated data to a dict
                    delta_dict: dict[str, str] = json.loads(response_data)

                    # if the dict is not None
                    if delta_dict != None:

                        # return the response data (merged with the first half of the response. Combined to a json dumps object)
                        yield json.dumps(first_half_of_response | delta_dict)

                except json.JSONDecodeError:

                    # catch but ignore the exception
                    pass

            # reset the response data for the next iteration
            response_data = ""
    
# Path: assets/scripts/api.py