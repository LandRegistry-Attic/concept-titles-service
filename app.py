from flask import Flask
from flask.ext import restful
import json
import os

app = Flask(__name__)
api = restful.Api(app)


def get_title(_id):
    result = None
    f = open('sample-data.json', 'r')
    titles = json.loads(f.read()) 
    for title in titles:
        if title['titleId'] == _id:
            result = title
            break
    return result

class TitleList(restful.Resource):
    def get(self):
        f = open('sample-data.json', 'r')
        return json.loads(f.read()) 

class Title(restful.Resource):
    def get(self, title_id):
        title = get_title(title_id)
        if title: 
            return title
        else:
            restful.abort( 404 ) 

api.add_resource(TitleList, '/titles')
api.add_resource(Title, '/titles/<string:title_id>')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)