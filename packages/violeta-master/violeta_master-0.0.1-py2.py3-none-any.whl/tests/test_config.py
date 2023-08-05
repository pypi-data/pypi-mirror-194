# coding : utf-8

import unittest
import os
from violeta.config import config, config_dir, tests_path


class TestConfigSections(unittest.TestCase):
	"""
	Test sections file config.ini
	"""
	def setUp(self):
		self.config = config['tests']
		self.path_json = '/tests/json_file/testjson.json'
		self.path_schema = '/tests/schema_file/testschema.json'
		self.path_xml = '/tests/xml_file/testxmltag.xml'
		self.formatter_json_path = ''.join([tests_path, self.config['path_json_file']])
		self.formatter_schema_path = ''.join([tests_path, self.config['path_schema_file']])
		self.formatter_xml_path = ''.join([tests_path, self.config['path_xml_file']])

	def tearDown(self):
		del self.config
		del self.path_json
		del self.path_schema
		del self.path_xml
		del self.formatter_json_path
		del self.formatter_schema_path
		del self.formatter_xml_path

	def test_json_path_file(self):
		self.assertEqual(self.config['path_json_file'], self.path_json)

	def test_schema_path_file(self):
		self.assertEqual(self.config['path_schema_file'], self.path_schema)

	def test_xml_path_file(self):
		self.assertEqual(self.config['path_xml_file'], self.path_xml)

	def test_formatter_path_json(self):
		self.assertIn(tests_path, self.formatter_json_path)
		self.assertIn(self.config['path_json_file'], self.formatter_json_path)

	def test_formatter_path_xml(self):
		self.assertIn(tests_path, self.formatter_xml_path)
		self.assertIn(self.config['path_xml_file'], self.formatter_xml_path)

	def test_formatter_path_schema(self):
		self.assertIn(tests_path, self.formatter_schema_path)
		self.assertIn(self.config['path_schema_file'], self.formatter_schema_path)


class TestConfigFile(unittest.TestCase):
	'''
	Test config file
	'''
	def setUp(self):
		self.path_config = "violeta/violeta/config"

	def tearDown(self):
		del self.path_config

	def test_path_file_config(self):
		self.assertIn(self.path_config, config_dir)
	#
	# def test_env_environment(self):
	# 	self.assertEqual(env, "development")
