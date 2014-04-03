import os
# hack
os.environ['DATABASE_URL'] = 'sqlite:////tmp/test.db'
import app
import unittest
import tempfile
import json

class HomeTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        #app.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def test_empty_titles(self):
        rv = self.app.get('/titles')
        self.assertEqual(json.loads(rv.data), {'titles': []})


    def test_titles_revisions(self):
        rv = self.app.post('/titles-revisions', data=json.dumps({
            "content": {
                "title_id": "AB1234",
                "address": "123 Fake St",
            },
        }), content_type='application/json')
        rv = self.app.get('/titles')
        self.assertEqual(json.loads(rv.data), {
            'titles': [{
                "title_id": "AB1234",
                "address": "123 Fake St",
            }]
        })

    def test_titles_revisions_postcode(self):
        rv = self.app.post('/titles-revisions', data=json.dumps({
            "content": {
                "title_id": "AB1234",
                "address": "123 Fake St",
                "postcode": "KT23 3AA"
            },
        }), content_type='application/json')
        rv = self.app.get('/titles')
        self.assertEqual(json.loads(rv.data), {
            'titles': [{
                "title_id": "AB1234",
                "address": "123 Fake St",
                "postcode": "KT23 3AA"
            }]
        })        

    def test_titles_postcode_query(self):
        rv = self.app.post('/titles-revisions', data=json.dumps({
            "content": {
                "title_id": "AB1234",
                "address": "123 Fake St",
                "postcode": "KT23 3AA"
            },
        }), content_type='application/json')

        rv = self.app.get('/titles?postcode=KT23 3AA')
        self.assertEqual(json.loads(rv.data), {
            'titles': [{
                "title_id": "AB1234",
                "address": "123 Fake St",
                "postcode": "KT23 3AA"
            }]
        })        


    def test_titles_postcode_query_empty(self):
        rv = self.app.post('/titles-revisions', data=json.dumps({
            "content": {
                "title_id": "AB1234",
                "address": "123 Fake St",
                "postcode": "KT23 3AA"
            },
        }), content_type='application/json')

        rv = self.app.get('/titles?postcode=KT23 3AB')
        self.assertEqual(json.loads(rv.data), {
            'titles': []
        })        

if __name__ == '__main__':
    unittest.main()
