# -*- coding: utf-8 -*-
from pymongo import MongoClient

class Mongo():

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27011/")

    def get_client(self):
        return self.client["fakenews"]
