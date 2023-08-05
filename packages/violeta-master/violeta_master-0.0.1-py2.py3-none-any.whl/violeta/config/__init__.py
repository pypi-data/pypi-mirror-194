# coding: utf-8

import configparser
import os

config_dir = os.path.dirname(__file__)
tests_path = os.path.dirname(config_dir)

# env = os.getenv('ENV', 'development')
# env = (env if env.strip() != "" else 'development')

config = configparser.ConfigParser()
config.read(os.path.join(config_dir, 'config.ini'))
