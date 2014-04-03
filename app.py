from flask import Flask, request
from flask.ext import restful
from flask.ext.restful import reqparse
from flask.ext.sqlalchemy import SQLAlchemy
from flask import jsonify
import json
import os

app = Flask(__name__)
api = restful.Api(app)
if 'DATABASE_URL' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace('postgres://', 'postgresql+psycopg2://')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://titles:password@%s/titles' % os.environ['DB_1_PORT_5432_TCP'].replace('tcp://', '')
db = SQLAlchemy(app)

class TitleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_id = db.Column( db.String(80) )
    postcode = db.Column( db.String(15), index=True)
    content = db.Column( db.String(10000) )

    def __init__(self, titleId, postcode, content ):
        self.title_id = titleId
        self.postcode = postcode
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
        try:
            title_id = request.json["content"]["title_id"]

        except:
            return "", 400

        try:
            raw_postcode = request.json["content"]["postcode"]
            postcode = raw_postcode.replace(" ", "")
        except:
            postcode = ""

        title = TitleModel(title_id, postcode, json.dumps(request.json["content"]))

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
        if 'postcode' in request.args:
            raw_postcode = request.args['postcode']
            postcode = raw_postcode.replace(" ", "")
            titles = TitleModel.query.filter_by( postcode = postcode)
            return jsonify( titles = [i.serialize['title'] for i in titles] ) 
        else:   
            titles = TitleModel.query.all()
            return jsonify( titles = [i.serialize['title'] for i in titles] )



api.add_resource(TitleRevisions, '/titles-revisions')
api.add_resource(Title, '/titles/<string:title_id>')
api.add_resource(TitleList, '/titles')
db.create_all()

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
