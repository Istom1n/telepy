__author__ = "Ivan Istomin, Ilya Gulkov"
__copyright__ = "Copyright 2018"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Ivan Istomin"
__email__ = "istom1n@pm.me"
__status__ = "Development"

import json
import os
import sys
from ctypes import (CDLL, CFUNCTYPE, c_char_p, c_double, c_int, c_longlong,
                    c_void_p)
from ctypes.util import find_library


class Telepy:
    # Check on loaded DLL
    _tdjson = None
    
    def __init__(self):
        """Return loaded tdlib instance."""
        if Telepy._tdjson is None:
            tdjson_path = os.path.dirname(os.path.realpath(__file__)) + "/lib/amd64_macos.dylib"

            if tdjson_path is None:
                print("Can't find tdjson library")
                quit()

            Telepy._tdjson = CDLL(tdjson_path)
            self.init_c_function()

        print(Telepy.td_json_client_destroy)
        
        Telepy.td_set_log_verbosity_level(2)
        Telepy.td_set_log_fatal_error_callback(
            Telepy.fatal_error_callback_type(
                Telepy.on_fatal_error_callback
                ))

        # Create client
        self.client = Telepy.td_json_client_create()


    @classmethod
    def init_c_function(cls):
        """Initialize Python wrapper for library function."""
        cls.td_json_client_create = cls._tdjson.td_json_client_create
        cls.td_json_client_create.restype = c_void_p
        cls.td_json_client_create.argtypes = []

        cls.td_json_client_receive = cls._tdjson.td_json_client_receive
        cls.td_json_client_receive.restype = c_char_p
        cls.td_json_client_receive.argtypes = [c_void_p, c_double]

        cls.td_json_client_send = cls._tdjson.td_json_client_send
        cls.td_json_client_send.restype = None
        cls.td_json_client_send.argtypes = [c_void_p, c_char_p]

        cls.td_json_client_execute = cls._tdjson.td_json_client_execute
        cls.td_json_client_execute.restype = c_char_p
        cls.td_json_client_execute.argtypes = [c_void_p, c_char_p]

        cls.td_json_client_destroy = cls._tdjson.td_json_client_destroy
        cls.td_json_client_destroy.restype = None
        cls.td_json_client_destroy.argtypes = [c_void_p]

        cls.td_set_log_file_path = cls._tdjson.td_set_log_file_path
        cls.td_set_log_file_path.restype = c_int
        cls.td_set_log_file_path.argtypes = [c_char_p]

        cls.td_set_log_max_file_size = cls._tdjson.td_set_log_max_file_size
        cls.td_set_log_max_file_size.restype = None
        cls.td_set_log_max_file_size.argtypes = [c_longlong]

        cls.td_set_log_verbosity_level = cls._tdjson.td_set_log_verbosity_level
        cls.td_set_log_verbosity_level.restype = None
        cls.td_set_log_verbosity_level.argtypes = [c_int]

        cls.fatal_error_callback_type = CFUNCTYPE(None, c_char_p)

        cls.td_set_log_fatal_error_callback = cls._tdjson.td_set_log_fatal_error_callback
        cls.td_set_log_fatal_error_callback.restype = None
        cls.td_set_log_fatal_error_callback.argtypes = [cls.fatal_error_callback_type]


    def download_library(self):
        """Download library binari of TDLib for current OS."""
        pass

    @staticmethod
    def on_fatal_error_callback(error_message):
        """Callback function for log with desired parameters."""
        print('TDLib fatal error: ', error_message)


    # Wrappers for client usage
    def td_send(self, query):
        query = json.dumps(query).encode('utf-8')
        Telepy.td_json_client_send(self.client, query)

    def td_receive(self):
        result = Telepy.td_json_client_receive(self.client, 1.0)
        if result:
            result = json.loads(result.decode('utf-8'))

        return result

    def td_execute(self, query):
        query = json.dumps(query).encode('utf-8')
        result = Telepy.td_json_client_execute(self.client, query)
        if result:
            result = json.loads(result.decode('utf-8'))

        return result

    def test(self):
        # Testing TDLib execute method
        print(self.td_execute({'@type': 'getTextEntities', 'text': '@telegram /test_command https://telegram.org telegram.me', '@extra': ['5', 7.0]}))

        # Testing TDLib send method
        print(self.td_send({'@type': 'getAuthorizationState', '@extra': 1.01234}))

    def __del__(self):
        """Destroy client when it is closed and isn't needed anymore."""
        self.td_json_client_destroy(self.client)


telepy = Telepy()

# Main events cycle
for i in range(5):
    event = telepy.td_receive()

    # If client is closed, we need to destroy it and create new client
    if event and event['@type'] is 'updateAuthorizationState' and event['authorization_state']['@type'] is 'authorizationStateClosed':
        break

    # Handle an incoming update or an answer to a previously sent request
    print(event)
    sys.stdout.flush()
