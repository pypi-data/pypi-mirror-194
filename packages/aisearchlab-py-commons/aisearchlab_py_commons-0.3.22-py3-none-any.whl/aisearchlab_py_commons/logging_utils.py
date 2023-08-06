"""
Logging utils
"""
from functools import wraps
from logging import StreamHandler, INFO, Formatter, Logger, Handler, \
    getLogger
from typing import Callable

from google.cloud.logging import Client
from google.cloud.logging.handlers import CloudLoggingHandler
from google.cloud.logging.resource import Resource
from google.oauth2.service_account import Credentials
from requests import get
from singleton_decorator import singleton


@singleton
class LoggingManager(object):
    """
    Logging manager
    """

    def __init__(self, project: str, dataset: str,
                 credentials: Credentials = None):
        """
        :param project: GCP project name
        :param dataset: dataset name
        :param credentials: Credentials.from_service_account_file(
        'service_account.json')
        """
        super().__init__()
        self._project = project
        self._dataset = dataset
        self._cred = credentials
        self._client = Client(
            project=self._project,
            credentials=self._cred)
        hostname = get('http://metadata/computeMetadata'
                       '/v1/instance/hostname',
                       headers={
                           'Metadata-Flavor': 'Google'
                       }).text.split('.')[0]
        zone = get('http://metadata/computeMetadata'
                   '/v1/instance/zone',
                   headers={
                       'Metadata-Flavor': 'Google'
                   }).text.split('/')[-1]
        resource = Resource(type="gce_instance", labels={
            'project_id': project,
            'instance_id': hostname,
            'zone': zone
        })
        handler = CloudLoggingHandler(client=self._client,
                                      name=dataset,
                                      resource=resource)
        self._handler = handler

    def get_cloud_handler(self) -> CloudLoggingHandler:
        """
        Returns cloud handler
        """
        return self._handler


def default_handler() -> Handler:
    """
    Returns default configured console handler
    """
    console = StreamHandler()
    console.setLevel(INFO)
    formatter = Formatter('[%(asctime)s] %(levelname)s %(name)s '
                          '%(threadName)s '
                          '{%(pathname)s:%(lineno)d} '
                          ' - %(message)s')
    console.setFormatter(formatter)
    return console


def log_in_out(logger: Logger,
               method_enter: Callable =
               lambda f, args, kwargs, log:
               log.info("Enter " + f.__name__),
               method_exit: Callable =
               lambda f, args, kwargs, log:
               log.info("Exit " + f.__name__)):
    """
    Logging decorator
    """

    def decorator(func):
        """
        Function decorator
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Decorated function
            """
            log = getLogger('log_in_out') \
                if logger is None else logger
            method_enter(func, args, kwargs, log)
            result = func(*args, **kwargs)
            method_exit(func, args, kwargs, log)
            return result

        return wrapper

    return decorator
