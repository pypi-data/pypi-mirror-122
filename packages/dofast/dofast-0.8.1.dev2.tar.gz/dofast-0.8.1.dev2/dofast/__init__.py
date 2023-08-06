from contextlib import contextmanager

from dofast.toolkits.textparser import TextParser
from dofast.utils import DeeplAPI
from dofast.weather import Weather
from dofast.pyavatar import PyAvataaar
from dofast.toolkits.qredis import QRedis


class AppInterfaces(object):
    def __init__(self):
        self.weather = Weather()
        self.textparser = TextParser
        self.deepl = DeeplAPI()
        self.avatar=PyAvataaar()
        self.redis=QRedis()



api = AppInterfaces()
