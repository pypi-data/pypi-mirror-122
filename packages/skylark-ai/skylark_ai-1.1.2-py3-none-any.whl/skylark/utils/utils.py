from skylark.constants.constants import WEBSOCKET_AUTH_API
import requests
import socket

def get_websocket_auth_token(token):
    try:
        '''
        changes --jash jain
        '''
        #changed the response so that when an api key(token) is passed a websocket token is retrieved
        response = requests.post(WEBSOCKET_AUTH_API,data={'api_key':token})
        if response.status_code == 201:
            print("hello")
            print(response.json())
            return response.json().get('key')
        else:
            return None
    except socket.gaierror:
        print("Internet not found")


def get_bytes_from_file(filename):
    return open(filename, "rb").read()
