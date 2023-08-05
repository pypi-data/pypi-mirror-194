# coding: utf-8

import jsonschema
import json
from xmltodict import parse as xml_parse
from xml.parsers.expat import ExpatError
from .base import BaseParser


class SimpleXMLParser(BaseParser):
    """
    Parser adequado para XML simples que possa facilmente ser convertido p/ um dict.
    A validacao é feita usando um jsonschema desses dados.
    """
    schema = None

    def __init__(self, payload, *, schema=None, **kwargs):
        if schema:
            self.schema = schema
        super(SimpleXMLParser, self).__init__(payload, **kwargs)

    def validate(self):

        try:
            data = xml_parse(self.payload.read())

        except ExpatError:
            raise Exception('O arquivo não é um JSON.')

        if self.schema:
            try:
                jsonschema.validate(data, self.schema)
            except jsonschema.ValidationError as e:
                raise Exception(e.message)

        return data
