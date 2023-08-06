import requests
import logging
import sys
import time
import datetime
import json
#both logging methods should work, need to test

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])

url = 'http://localhost:5000'

#Configure the url used by the application
def configUrl(newUrl):
    global url
    url = newUrl

def create_path(path, return_code, return_value, delay=0, headers=None):
    #Default header to utilize
    headers_data = {'Content-Type': "application/json"}
    # print(headers)
    #Check if additional header value is given
    if headers:
        #Data type validation
        if not isinstance(headers, dict):
            raise TypeError
        #Update headers dict --> can input many additional headers
        headers_data.update(headers)
    # print(headers_data)
    if isinstance(delay, str):
        try:
            delay = int(delay)
        except:
            TypeError

    #Json path, return_code, return_value, arbitrary delay
    path_configuration = {
        'path': path,
        'return_code': return_code,
        'return_value': return_value,
        'delay': delay,
        'headers': headers_data,
        'time_stamp': datetime.datetime.now().isoformat()
    }

    #Data validation:
    try:
        #request
        result = requests.post(url=url, headers={"Content-Type": "application/json"}, json=path_configuration)
        #logging
        logging.info('{}'.format(path_configuration))
        #return pass or fail
        if result.status_code != 200:
            print("\nPath creation Failed!\nStatus_code: {},\nUrl: {},\nError_text: {}".format(result.status_code, result.url, result.reason))
            #logging
            logging.warning("\nPath creation Failed!\nStatus_code: {},\nUrl: {},\nError_text: {}".format(result.status_code, result.url, result.reason))
            return "\nPath creation Failed!\nStatus_code: {},\nUrl: {},\nError_text: {}".format(result.status_code, result.url, result.reason)
    except TypeError as e:
        print(f"\nPath creation Failed! Error_text: Delay must be a numeric value. Delay is {path_configuration['delay']}")
        print(e)

def create_paths( path):
    for obj in path :
        #Verifying valid delay is present
        if "delay" not in obj :
            obj["delay"] = 0
        if not isinstance(obj["delay"], int):
            raise TypeError

        #Verifying valid headers are present
        headers_data = {'Content-Type': "application/json"}
        if "headers" not in obj:
            obj["headers"] = headers_data
        else:
            if not isinstance(obj["headers"], dict):
                raise TypeError
            obj["headers"].update(headers_data)
            logging.info('Header Data: {}'.format(obj["headers"]))

        result = requests.post(url=url, headers=obj["headers"], json=obj)
        #logging
        logging.info('{}, created'.format(path))

        #return pass or fail
        if result.status_code != 200:
            print("\nPaths creation Failed!\nStatus_code: {},\nUrl: {},\nError_text: {}".format(result.status_code, result.url, result.reason))
            #logging
            logging.warning("\nPaths creation Failed!\nStatus_code: {},\nUrl: {},\nError_text: {}".format(result.status_code, result.url, result.reason))

def get_path(path):
    try:
        #retrieve json data from Flask web server
        data = requests.get(url, path).json()
        for path_data in data:
            path_data = json.loads(path_data)
            if path_data['name'] == path:
                logging.info('{}, returned value'.format(path_data))
                return path_data

        #logging
    except KeyError:
        print(path + " doesn't exist.")
        logging.warning("{}, doesn't exist.".format(path))

def get_all():
    data = requests.get(url, "/")
    return data.json()

def update_path( path, rc, return_value, delay=0, headers=None):
    create_path(path, rc, return_value, delay, headers)
    #logging
    logging.info('Endpoint updated')

def delete_path( path):
    try:
        requests.delete(url, json={"path" : path})
        # logging
        logging.info("Endpoint Deleted, {}".format(path))
    except KeyError:
        #logging
        logging.warning("No Endpoint match")

def delete_paths(paths):
    logging.info("List of endpoints sent to be deleted, {}".format(paths))
    response = requests.delete(url, json=paths)
    # print(response.content)
    if response.status_code >= 400:
        # print('error')
        logging.info("One or more of these paths do not exist!")
        logging.error(response.status_code)
        logging.error(response.reason)
        print(response.content)
        return response.content
    if response.status_code < 300 and response.status_code >= 200:
        logging.info("All paths successfully deleted")
        return response.content
