__author__ = "Ivan Istomin, Ilya Gulkov"
__copyright__ = "Copyright 2018"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Ivan Istomin"
__email__ = "istom1n@pm.me"
__status__ = "Development"

import json
import os
import platform
import sys
from ctypes import (CDLL, CFUNCTYPE, c_char_p, c_double, c_int, c_longlong,
                    c_void_p)

import api_methods


class Telepy:
    # Check on loaded DLL
    _tdjson = None
    _platforms = {
        'Darwin': {'x86_64': 'x86_64_macos.dylib'},
        # TODO Compile and upload libs for windows
        # 'Windows': {'32bit': '', '64bit': ''},
        'Linux': {'x86_64': 'x86_64_linux.so', 'i686': 'i686_linux.so'}
    }
    

    def __init__(self):
        """Return loaded TDLib instance."""
        if Telepy._tdjson is None:

            uname_result = platform.uname()
            
            tdjson_path = '{}/lib/{}'.format(os.path.dirname(os.path.realpath(
                __file__)), Telepy._platforms[uname_result[0]][uname_result[4]])
            
            if tdjson_path is None:
                print("Can't find tdjson library")
                quit()
            
            Telepy._tdjson = CDLL(tdjson_path)
            self.init_c_client_functions()
            self.init_c_log_functions()
        
        Telepy.td_set_log_verbosity_level(2)

        print(Telepy.td_json_client_destroy)

        # Create client
        self.client = Telepy.td_json_client_create()

    def __del__(self):
        """Destroy client when it is closed and isn't needed anymore."""
        Telepy.td_json_client_destroy(self.client)

    @classmethod
    def init_c_client_functions(cls):
        """Initialize Python wrapper for library clent functions."""

        """
        Creates a new instance of TDLib.
        """
        cls.td_json_client_create = cls._tdjson.td_json_client_create
        cls.td_json_client_create.restype = c_void_p
        cls.td_json_client_create.argtypes = []

        """
        Receives incoming updates and request responses from the TDLib client.
        May be called from any thread, but shouldn't be called simultaneously from two
        different threads. Returned pointer will be deallocated by TDLib during next call
        to td_json_client_receive or td_json_client_execute in the same thread, so it
        can't be used after that.
        """
        cls.td_json_client_receive = cls._tdjson.td_json_client_receive
        cls.td_json_client_receive.restype = c_char_p
        cls.td_json_client_receive.argtypes = [c_void_p, c_double]

        """
        Sends request to the TDLib client. May be called from any thread.
        """
        cls.td_json_client_send = cls._tdjson.td_json_client_send
        cls.td_json_client_send.restype = None
        cls.td_json_client_send.argtypes = [c_void_p, c_char_p]

        """
        Synchronously executes TDLib request. May be called from any thread.
        Only a few requests can be executed synchronously. Returned pointer will be deallocated
        by TDLib during next call to td_json_client_receive or td_json_client_execute in the same
        thread, so it can't be used after that.
        """
        cls.td_json_client_execute = cls._tdjson.td_json_client_execute
        cls.td_json_client_execute.restype = c_char_p
        cls.td_json_client_execute.argtypes = [c_void_p, c_char_p]

        """
        Destroys the TDLib client instance. After this is called the client
        instance shouldn't be used anymore.
        """
        cls.td_json_client_destroy = cls._tdjson.td_json_client_destroy
        cls.td_json_client_destroy.restype = None
        cls.td_json_client_destroy.argtypes = [c_void_p]

    @classmethod
    def init_c_log_functions(cls):
        """Initialize Python wrapper for library log functions."""

        """
        Sets the path to the file where the internal TDLib log will be written.
        By default TDLib writes logs to stderr or an OS specific log. Use this method
        to write the log to a file instead.
        """
        cls.td_set_log_file_path = cls._tdjson.td_set_log_file_path
        cls.td_set_log_file_path.restype = c_int
        cls.td_set_log_file_path.argtypes = [c_char_p]

        """
        Sets maximum size of the file to where the internal TDLib log is written before
        the file will be auto-rotated. Unused if log is not written to a file. Defaults
        to 10 MB.
        """
        cls.td_set_log_max_file_size = cls._tdjson.td_set_log_file_path
        cls.td_set_log_max_file_size.restype = None
        cls.td_set_log_max_file_size.argtypes = [c_longlong]

        """
        Sets the verbosity level of the internal logging of TDLib. By default the
        TDLib uses a log verbosity level of 5.
        """
        cls.td_set_log_verbosity_level = cls._tdjson.td_set_log_file_path
        cls.td_set_log_verbosity_level.restype = None
        cls.td_set_log_verbosity_level.argtypes = [c_int]

        """
        Sets the callback that will be called when a fatal error happens. None of the TDLib
        methods can be called from the callback. The TDLib will crash as soon as callback returns.
        By default the callback is not set.
        """
        cls.fatal_error_callback_type = CFUNCTYPE(None, c_char_p)

        cls.td_set_log_fatal_error_callback = cls._tdjson.td_set_log_fatal_error_callback
        cls.td_set_log_fatal_error_callback.restype = None
        cls.td_set_log_fatal_error_callback.argtypes = [
            cls.fatal_error_callback_type]

    def download_library(self):
        # TODO Download library binari of TDLib for current OS.
        pass

    
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

    @staticmethod
    def on_fatal_error_callback(error_message):
        """Callback function for log with desired parameters."""
        print('TDLib fatal error: ', error_message)

    def test(self):
        # Testing TDLib execute method
        print(
            self.td_execute(
                {
                    api_methods.getTextEntities('@telegram /test_command https://telegram.org telegram.me')
                }
            )
        )

        # Testing TDLib send method
        self.td_send({'@type': 'getAuthorizationState', '@extra': 1.01234})

    # def __getitem__(self, key):
    #     return self


if __name__ == '__main__':
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
