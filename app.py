from flask import Flask
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
    titleId = db.Column( db.String(80), unique=True)

    def __init__(self, titleId ):
        self.titleId = titleId

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'titleId': self.titleId
       }


class TitleList(restful.Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(TitleList, self).__init__()

    def get(self):
        titles = TitleModel.query.all()
        return jsonify(json_list=[i.serialize for i in titles])

    def post(self):
        #TODO Add regex validation for title id
        self.parser.add_argument('titleId', type=str, required=True, location='json', help="Invalid Title Id format")
        args = self.parser.parse_args()
        title = TitleModel(args['titleId'])
        db.session.add( title )
        db.session.commit()
        return "", 201
    


class Title(restful.Resource):
    def get(self, title_id):
        titles = TitleModel.query.filter_by( titleId = title_id)        
        return jsonify( json_list=[i.serialize for i in titles] )


api.add_resource(TitleList, '/titles')
api.add_resource(Title, '/titles/<string:title_id>')
db.create_all()

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)