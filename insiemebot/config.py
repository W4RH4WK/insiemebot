import os
import logging

from xdg.BaseDirectory import xdg_config_home
from configparser import ConfigParser


DEFAULT_CONFIG_FILE = os.path.join(xdg_config_home, "insiemebot", "insiemebot.cfg")
DEFAULT_CONFIG = { 'token': '' }
TOP_SECTION = 'base'


class Config:

    def __init__(self, config_file=DEFAULT_CONFIG_FILE, auto_load=True,
                       create_default=True):
        self.config_file = config_file

        self.data = ConfigParser()
        self.data[TOP_SECTION] = DEFAULT_CONFIG

        if os.path.exists(self.config_file):
            if auto_load:
                self.load()
        else:
            if create_default:
                self.save()


    def __getitem__(self, key):
        return self.data[TOP_SECTION][key]


    def __setitem__(self, key, value):
        self.data[TOP_SECTION][key] = value


    def __contains__(self, key):
        return key in self.data


    def load(self):
        logging.info('Loading config from %s', self.config_file)
        self.data.read(self.config_file)


    def save(self):
        logging.info('Saving config to %s', self.config_file)
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            self.data.write(f)
