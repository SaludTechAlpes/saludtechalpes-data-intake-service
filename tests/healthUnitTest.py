import unittest
from flask import Flask
from flask_restful import Api
from http import HTTPStatus
from src import create_app

class TestHealth(unittest.TestCase):

    def setUp(self):

        self.app = create_app('test')
        self.api = Api(self.app)
        self.client = self.app.test_client()  

    def test_get_health(self):
        response = self.client.get('/health')

        self.assertEqual(response.status_code, HTTPStatus.OK)