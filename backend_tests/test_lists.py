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
        self.assertEqual(data['name'], "AWS Certified Solutions Architect Associate Certification")
    
    def test_post_list_create(self):
       #register and login a user
        response = self.client.post('/auth/register', data={
            'username': 'tester',
            'password': '123456'
        })
        # print(response.data)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/auth/login', data={
            'username': 'tester',
            'password': '123456'
        }, follow_redirects=True)
        # print(response.data)
        self.assertEqual(response.status_code, 200)

        #creating the data for the list
        list_data = {
            "name": "Greatest dev project",
            "description": "Greatest dev project"
        }
        #the POST request with the url, the list data and the token
        response = self.client.post("lists/",
        data = list_data)
        #print(response)
        #get the JSON object of the new list
        data = response.get_json()
        #print(data)
        #check if we now have a list with that ID in the lists table
        list = List.query.get(data["id"])
        #test the 200 status
        self.assertEqual(response.status_code, 200)
        #test there's some data in the response
        self.assertIsNotNone(list)
        self.assertEqual(list.name, "Greatest dev project")
    
    #POST method in /lists not allowed
    def test_post_list_create_not_allowed(self):
        #login the user that already owns a list
        response = self.client.post('/auth/login', data={
            'username': 'Gabe',
            'password': '123456'
        }, follow_redirects=True)
        #print(response.data)
        self.assertEqual(response.status_code, 200)

        #creating the data for the list
        list_data = {
            "name": "Greatest dev project",
            "description": "Greatest dev project"
        }
        #the POST request with the url, the list data and the token
        response = self.client.post("lists/",
        data = list_data)

        #test a 400 status, a user that already has a list cannot post a new one
        self.assertEqual(response.status_code, 400)

    # #DELETE method in lists/id, not allowed to delete
    def test_delete_list_not_allowed(self):
        #register and login a user
        response = self.client.post('/auth/register', data={
            'username': 'tester',
            'password': '123456'
        })
        
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/auth/login', data={
            'username': 'tester',
            'password': '123456'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        #get the first list
        list = List.query.first()
        #try to delete it
        response = self.client.get(f"lists/delete/{list.id}")
        #test a 400 status, a user is not the owner of the list cannot delete it
        self.assertEqual(response.status_code, 400)

    # #DELETE method on /lists/id allowed
    def test_delete_list_allowed(self):
        #login a user that already exists and get the token
        #login the user that already owns a list
        response = self.client.post('/auth/login', data={
            'username': 'Gabe',
            'password': '123456'
        }, follow_redirects=True)
        #print(response.data)
        self.assertEqual(response.status_code, 200)

        list = List.query.first()
        response = self.client.get(f"lists/delete/{list.id}")
        # print(response.data)
        #test the OK status
        self.assertEqual(response.status_code, 200)
        #query to the list we deleted
        list_del = List.query.get(list.id)
        #test that none has been received
        self.assertIsNone(list_del)
