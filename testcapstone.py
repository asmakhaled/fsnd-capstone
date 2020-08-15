import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db

class CapstoneTest(unittest.TestCase):
    def setUp(self):
        self.sales_token = os.environ['sales_token']
        self.supervisor_token = os.environ['supervisor_token']
        self.manager_token = os.environ['manager_token']
        self.app = create_app()
        self.client = self.app.test_client

        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def make_request_with_token(self, token):
        res = self.client().get('/reviewers', headers={
            "Authorization": 'bearer ' + token})
        body = json.loads(res.data)
        return body

    # Reviewers Tests
    def test_get_reviewers_with_sales_authentication_success(self):
        res = self.client().get('/reviewers', headers={
            "Authorization": 'bearer '+self.sales_token})
        body = self.make_request_with_token(self.sales_token)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_get_reviewers_with_supervisor_authentication_success(self):
        res = self.client().get('/reviewers', headers={
            "Authorization": 'bearer '+self.supervisor_token})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_get_reviewers_with_manager_authentication_success(self):
        res = self.client().get('/reviewers', headers={
            "Authorization": 'bearer '+self.manager_token})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    # Assignments tests
    def test_get_assignments_with_authentication_success(self):
        res = self.client().get('/assignments', headers={
            "Authorization": 'bearer '+self.manager_token})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    # Projects tests
    def test_get_projects_with_authentication_success(self):
        res = self.client().get('/projects', headers={
            "Authorization": 'bearer '+self.sales_token})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

if __name__ == "__main__":
    unittest.main()
