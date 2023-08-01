#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/scientists', methods = ['GET', 'POST'])
def scientists():
    if(request.method == 'GET'): 
        all = Scientist.query.all()
        return [scientist.to_dict(rules = ('-missions',)) for scientist in all], 200 
    else: 
        data = request.json 
        scientist = Scientist()
        try: 
            for attr in data: 
                setattr(scientist, attr, data[attr])
            db.session.add(scientist)
            db.session.commit()
            return scientist.to_dict(rules = ('-missions',)), 201
        except ValueError as ie: 
            return {'error' : ie.args}, 400
        
@app.route('/scientists/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def scientists_by_id(id): 
    scientist = Scientist.query.filter(Scientist.id == id).first()
    if not scientist: 
        return {'error': 'scientist not found'}, 404
    if(request.method == 'GET'):
        return scientist.to_dict(rules = ('missions',)), 200
    if(request.method == 'PATCH'):
        data = request.json 
        try: 
            for attr in data: 
                setattr(scientist, attr, data[attr])
            db.session.add(scientist)
            db.session.commit()
            return scientist.to_dict(rules = ('-missions',)), 202
        except ValueError as ie: 
            return {'error': '[validation errors]'}, 400
    if(request.method == 'DELETE'):
            db.session.delete(scientist)
            db.session.commit()
            return {}, 200
        
@app.route('/planets')
def planets():
        all = Planet.query.all()
        return [planet.to_dict(rules = ('-missions',)) for planet in all], 200 
    
   
@app.route('/missions', methods = ['POST'])
def missions():
    if(request.method == 'POST'): 
        data = request.json 
        mission = Mission()
        try: 
            for attr in data: 
                setattr(mission, attr, data[attr])
            db.session.add(mission)
            db.session.commit()
            return mission.to_dict(rules = ('scientists', 'planets')), 201
        except ValueError as ie: 
            return {'error' : ie.args}, 400
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)
