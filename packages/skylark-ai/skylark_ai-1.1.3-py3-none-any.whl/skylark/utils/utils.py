from skylark.constants.constants import WEBSOCKET_AUTH_API
import requests
import socket
REMOTE_SERVER = "one.one.one.one"

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

def is_connected(hostname="one.one.one.one"):
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except:
     pass
  return False
