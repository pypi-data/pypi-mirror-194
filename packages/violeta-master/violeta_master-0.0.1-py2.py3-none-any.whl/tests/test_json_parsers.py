# coding: utf-8

import unittest
import json
from violeta.parsers import JsonParser
import os

config_dir = os.path.dirname(__file__)


tests_json = os.path.join(config_dir, 'json_file', 'testjson.json')
tests_schema = os.path.join(config_dir, 'schema_file', 'testschema.json')


class TestJsonParser(unittest.TestCase):
    '''
    Test Json Parser Schema validation
    '''

    def setUp(self):
        self.schema_file = open(''.join([tests_schema]), 'r')
        self.schema_data = json.load(self.schema_file)
        self.json_file = open(''.join([tests_json]), 'r')
        self.json_data = json.load(self.json_file)

    def tearDown(self):
        del self.json_data
        del self.schema_data
        del self.schema_file

    def test_parser_data_json_validate(self):
        json_validate = JsonParser(self.json_data, schema=self.schema_data).validate()
        self.assertEqual(json_validate, self.json_data)

    def test_parser_data_json_error_validate(self):
        del self.json_data['root']['titulos']
        self.assertRaises(Exception, JsonParser(self.json_data, schema=self.schema_data).validate)
