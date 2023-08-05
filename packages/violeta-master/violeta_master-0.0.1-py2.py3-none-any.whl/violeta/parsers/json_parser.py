# coding: utf-8

import json
import jsonschema
from .base import BaseParser


class JsonParser(BaseParser):
    schema = None  # poderia ser sobrescrito em subclasses para n precisar passar o schema sempre

    def __init__(self, payload, *, schema=None, **kwargs):
        self.schema = schema or self.schema
        super(JsonParser, self).__init__(payload, **kwargs)

    def validate(self):
        data = self.payload
        if not isinstance(self.payload, dict):
            try:
                data = json.load(self.payload)
            except json.decoder.JSONDecodeError:
                raise Exception('O arquivo não é um json')

        if self.schema:
            try:
                jsonschema.validate(data, self.schema)
            except jsonschema.ValidationError as error:
                raise Exception(error.message)

        return data
