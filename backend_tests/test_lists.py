import unittest
import os
from models.List import List
from main import create_app, db

class TestLists(unittest.TestCase):
    #Runs before the tests
    @classmethod
    def setUp(cls):
        if os.environ.get("FLASK_ENV") != "testing":
            raise EnvironmentError("FLASK_ENV is not testing")
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

        db.create_all()

        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db", "seed"])

    #runs after all the tests, removes the tables and stops the app
    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    # test the GET method in /lists/ returns all the lists
    def test_get_all_lists(self):
        response = self.client.get("/lists/")

        data = response.get_json()
        # print(data)
        #check the OK status
        self.assertEqual(response.status_code, 200)
        #the response data is a list
        self.assertIsInstance(data, list)
        #the length of the list is 2, we know that because we seeded the data
        self.assertEqual(len(data), 3)

    def test_get_lists_by_id(self):
        #get the first list from the db -> id=1
        list = List.query.first()
        response = self.client.get(f"/lists/{list.id}")

        data = response.get_json()
        # print(data)
         #check the OK status
        self.assertEqual(response.status_code, 200)
        #the response data is a dict
        self.assertIsInstance(data, dict)
        #test a value of the response, as we seeded the data we know that value
        self.assertEqual(data['name'], "AWS Certified Solutions Architect – Associate Certification")
    


