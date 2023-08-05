# coding: utf-8

import unittest
import json
from xmltodict import parse
from violeta.parsers import SimpleXMLParser
import os

config_dir = os.path.dirname(__file__)


tests_json = os.path.join(config_dir, 'json_file', 'testjson.json')
tests_schema = os.path.join(config_dir, 'schema_file', 'testschema.json')
tests_xml = os.path.join(config_dir, 'xml_file', 'testxmltag.xml')


class TestXmlParser(unittest.TestCase):
    '''
    Test xml parser schema validation
    '''

    def setUp(self):
        self.schema_file = open(''.join([tests_schema]), 'r')
        self.schema_data = json.load(self.schema_file)
        self.json_file = open(''.join([tests_schema]), 'r')
        self.json_data = json.load(self.json_file)
        self.xml_file = open(''.join([tests_xml]), 'r')

    def tearDown(self):
        del self.schema_file
        del self.schema_data
        del self.json_file
        del self.json_data
        del self.xml_file

    def test_parser_file_xml_validate(self):
        xml_validate = SimpleXMLParser(self.xml_file, schema=self.schema_data).validate()
        xml_check = open(''.join([tests_xml]), 'r')
        self.assertEqual(parse(xml_check.read()), xml_validate)
