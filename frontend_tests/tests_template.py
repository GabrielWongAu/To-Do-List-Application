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
        runner.invoke(args=["db-custom", "seed"])

    #runs after all the tests, removes the tables and stops the app
    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    #GET method in /lists/
    def test_list_index(self):
        #response is going to contain the html with all the lists
        response = self.client.get("/lists/")
        print(response.data)
        #get all the lists from the database
        lists = List.query.all()
        #print(lists[0].name)
        self.assertEqual(response.status_code, 200)
        #test content from the layout
        self.assertIn("Prepare for HashiCorp Cloud Engineer Certification Terraform Associate", str(response.data))
        #test if the html contains the names and descriptions of the lists
        self.assertIn(lists[1].name, str(response.data))
        self.assertIn(lists[2].name, str(response.data))

    def test_list_by_id(self):
        list = List.query.first()
        response = self.client.get(f"/lists/{list.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Back", str(response.data))
        self.assertIn(list.name, str(response.data))
        self.assertIn(list.description, str(response.data))
