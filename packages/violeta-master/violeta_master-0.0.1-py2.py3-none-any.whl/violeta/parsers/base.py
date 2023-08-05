# coding: utf-8

from abc import ABCMeta, abstractmethod


class BaseParser(metaclass=ABCMeta):
    data_validation = None

    def __init__(self, payload, func=None):
        if not hasattr(payload, 'read') and not isinstance(payload, dict):
            raise Exception("'payload' deve ser um objeto file-like or dict")

        self.payload = payload
        if func:
            self.data_validation = func

    @abstractmethod
    def validate(self):
        pass

    def parse(self):

        data = self.validate()

        if self.data_validation:
            return self.data_validation(data)
        return data
