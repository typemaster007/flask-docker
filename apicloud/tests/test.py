import sys
sys.path.append('E:/Cloud_Computing/Assignment3/Flaskapp/flask-docker/apicloud')
import app
from app import app 
from app import add_note, add_catalogue
import json

from pymongo import MongoClient

import unittest 

class UnitTestcase(unittest.TestCase): 

    @classmethod
    def setUpClass(cls):
        pass 

    @classmethod
    def tearDownClass(cls):
        pass 

    def setUp(self):
                                              # creates a test client
        self.app = app.test_client()
        self.app.testing = True 

    def tearDown(self):
        pass 

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/') 

        # assert the status code of the response
        self.assertEqual(result.status_code, 200) 

    def test_positive_search_result_data(self):
        
        result = self.app.get('/results?search=Charles&time=2020-03-18+21%3A02%3A40.356739&freqcount=0') 
        #print("Result =",result.data)
        self.assertTrue(b'Hypatia' in result.data)

    def test_no_results_found(self):
        
        result = self.app.get('/results?search=Charles2', follow_redirects='True') 
        #print("Result =",result.data )
        self.assertTrue(b'No Query results found, re-enter' in result.data)


        #Check if database connects successfully and has data
    def test_mongo_connect1(self):
        myclient = MongoClient("mongodb://localhost:27017/")
        mydb = myclient["gutenberg"]
        mycol = mydb["books"]
        myquery = { "Author": "Charles" }
        myquery2 = { "Author": "NotCharles" }
        test = mycol.find_one(myquery)
        test2 = mycol.find_one(myquery2)
        #print("Result =",test )
        self.assertTrue(test)
        self.assertFalse(test2)

        #Check if database connects successfully and has data
    def test_mongo_connect_negative(self):
        myclient = MongoClient("mongodb://localhost:27017/")
        mydb = myclient["gutenberg1"]
        mycol = mydb["books2"]
        myquery = { "Author": "Charles" }
        myquery2 = { "Author": "NotCharles" }
        test = mycol.find_one(myquery)
        test2 = mycol.find_one(myquery2)
        #print("Result =",test )
        self.assertFalse(test)
        self.assertFalse(test2)
    
    def test_add_retreive_notes(self):
        ret = []
        search = 'Charles'
        note = 'This is a sample note. Unit testing case 7.'
        notefound = False
        add_note(search,note)
        with open('file.json') as f:
          for line in f:
            ret.append(json.loads(line))
        for i in ret:
            if (i['Note']=='This is a sample note. Unit testing case 7.') :
              #print("note = ", i['Note'])
              notefound = True
        self.assertTrue(notefound)

    def test_Catalogue(self):
        ret = []
        search = 'Charles'
        myclient = MongoClient("mongodb://localhost:27017/")
        mydb = myclient["gutenberg"]
        mycol = mydb["books"]
        myquery = { "Author": "Charles" }
        doc = mycol.find(myquery)
        catalogfound = False
        add_catalogue(search,doc)
        with open('catalogue.json') as cat:
          for line in cat:
            ret.append(json.loads(line))
        cat.close
        for i in ret:
            if (i['Author']=='Charles'):
              catalogfound = True
        self.assertTrue(catalogfound)

    
