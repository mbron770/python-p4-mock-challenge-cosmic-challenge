from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    # Add relationship
    
    missions = db.relationship('Mission', cascade = 'all, delete, delete-orphan', back_populates = 'planet')
    
    # Add serialization rules 
    serialize_rules = ('-missions.planet',)
    

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)

    # Add relationship
    missions = db.relationship('Mission', cascade = 'all, delete, delete-orphan', back_populates = 'scientist')
    

    # Add serialization rules
    serialize_rules = ('-missions.scientist',)

    # Add validation
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 1: 
            raise ValueError('must have name')
        return name 
    
    @validates('field_of_study')
    def validate_field_of_study(self, key, field_of_study):
        if not field_of_study or len(field_of_study) < 1: 
            raise ValueError('must have field_of_study')
        return field_of_study 
        
   
    
    


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationships
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'))
    
    planet = db.relationship('Planet', back_populates = 'missions')
    scientist = db.relationship('Scientist', back_populates = 'missions')
   
    # Add serialization rules
    serialize_rules = ('-planet.missions', '-scientist.missions')
    

    # Add validation
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 1: 
            raise ValueError('must have name')
        return name 
    
    @validates('planet_id')
    def validate_planet_id(self, key, planet_id):
        if not planet_id: 
            raise ValueError('must have planet_id')
        return planet_id 
    
    @validates('scientist_id')
    def validate_scientist_id(self, key, scientist_id):
        if not scientist_id: 
            raise ValueError('must have scientist_id')
        return scientist_id
   


# add any models you may need.
