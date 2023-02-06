import os
import json


SETTINGS_FILE_NAME = 'settings.json'
CONF_DICT = {}


def load_configuration_from_json(_json_filepath = SETTINGS_FILE_NAME):
    """Load the configuration from the settings.json file"""
    global CONF_DICT
    try:
        with open(_json_filepath,'r') as conf_file:
            CONF_DICT = json.load(conf_file)['config']

    except Exception as e:
        raise Exception(f'Failed to load {_json_filepath} due to: {e}')


class Config(object):
    """Common generic configurations"""
    # ## Define the application directory
    # BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    #
    # ## Load configuration details from settings.json file
    # load_configuration_from_json(os.path.join(BASE_DIR, SETTINGS_FILE_NAME))

    ## HOST & PORT
    HOST = '127.0.0.1'
    PORT = 8008

    ## Version
    VERSION = 1.0

    ## URL Prefix
    URL_PREFIX = "api"

    ## Statement for enabling the development environment
    DEBUG = "true"

    ## Application threads
    THREADS_PER_PAGE = 2

    ## Enable protection against *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = "true"
    CSRF_SESSION_KEY = ""

class DevelopmentConfig(Config):
    '''
    Configuration specific to development environment
    '''
    ENV = "development"
    DEBUG = "true"
    DEVELOPMENT = "true"
    DB_HOST = "127.0.0.1"
    DB_PORT = 3306
    DB_USER = "undanga4_zen"
    DB_PASSWD = "ft,_DY3p.Ap!"
    DB_NAME = "undanga4_wedding"
    CONNECT_TIMEOUT = 5