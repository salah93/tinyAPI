'''context.py -- Provides mechanism for an application to determine in which
   environment it is running and what aspect of the application is executing.'''

__author__ = 'Michael Montero <mcmontero@gmail.com>'

# ----- Import ----------------------------------------------------------------

from .exception import ContextException
from tinyAPI.base.singleton import Singleton
import os

# ----- Private Functions -----------------------------------------------------

def __context_env_matches(env):
    return Context().get_server_env() == env

# ----- Public Functions ------------------------------------------------------

def env_local():
    return __context_env_matches(Context.LOCAL)

def env_staging():
    return __context_env_matches(Context.STAGING)

def env_qa():
    return __context_env_matches(Context.QA)

def env_prod():
    return __context_env_matches(Context.PRODUCTION)

def env_not_prod():
    return not __context_env_matches(Context.PRODUCTION)

def env_cli():
    return Context().is_cli()

def env_web():
    return Context().is_web()

def env_unit_test():
    return Context().is_unit_test()

# ----- Public Classes --------------------------------------------------------

class Context(metaclass=Singleton):
    '''Provides information about the context in which the application is
       running.'''

    LOCAL = 'local'
    STAGING = 'staging'
    QA = 'qa'
    PRODUCTION = 'production'

    def __init__(self):
        self.reset()

    def get_server_env(self):
        if self.__server_env is None:
            server_env = os.environ.get('APP_SERVER_ENV')
            if server_env is None:
                raise ContextException(
                        'could not find environment variable called '
                        + '"APP_SERVER_ENV"')

            if server_env not in [self.LOCAL,
                                  self.STAGING,
                                  self.QA,
                                  self.PRODUCTION]:
                raise ContextException(
                        'application server environment "'
                        + server_env
                        + '" is not valid')

            self.__server_env = server_env

        return self.__server_env

    def is_cli(self):
        return self.__is_cli

    def is_unit_test(self):
        return self.__is_unit_test

    def is_web(self):
        return self.__is_web

    def reset(self):
        self.__server_env = None
        self.__is_cli = False
        self.__is_web = False
        self.__is_unit_test = False

        if str(os.environ.get('ENV_UNIT_TEST')) == "1":
            self.__is_unit_test = True

    def set_cli(self):
        self.__is_cli = True
        return self

    def set_unit_test(self):
        self.__is_unit_test = True
        return self

    def set_web(self):
        self.__is_web = True
        return self

__all__ = ['Context', 'env_cli', 'env_local', 'env_not_prod', 'env_prod',
           'env_qa', 'env_staging', 'env_unit_test', 'env_web']