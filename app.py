from flask import Flask, request
from flask.ext import restful
from flask.ext.restful import reqparse
from flask.ext.sqlalchemy import SQLAlchemy
from flask import jsonify

import json
import os

app = Flask(__name__)
api = restful.Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class TitleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_id = db.Column( db.String(80) )
    content = db.Column( db.String(10000) )

    def __init__(self, titleId, content ):
        self.title_id = titleId
        self.content = content

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
       
           "title" : json.loads(self.content)
       
       }


class TitleRevisions(restful.Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(TitleRevisions, self).__init__()


    def post(self):
        content = json.loads(request.data)
        title_id = request.json["title_id"]

        title = TitleModel(title_id, request.data)


        existing = TitleModel.query.filter_by( title_id = title_id).first()  

        if existing:
            db.session.delete( existing )
            db.session.add( title )
        else:
            db.session.add( title )
        db.session.commit()
        return "", 201
    


class Title(restful.Resource):
    def get(self, title_id):
        title = TitleModel.query.filter_by( title_id = title_id).first()  

        if title:
            return jsonify( title.serialize )
        else:
            restful.abort( 404 )

class TitleList(restful.Resource):
    def get(self):
        titles = TitleModel.query.all()
        return jsonify( titles = [i.serialize for i in titles] )
      
api.add_resource(TitleRevisions, '/titles-revisions')
api.add_resource(Title, '/titles/<string:title_id>')
api.add_resource(TitleList, '/titles')

db.create_all()

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)