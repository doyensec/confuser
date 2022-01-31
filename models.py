from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

db = SQLAlchemy()


class Callback(db.Model):
    __tablename__ = "callbacks"
    id = db.Column(db.Integer, primary_key=True)
    protocol = db.Column(db.String)
    interactionString = db.Column(db.String)
    time = db.Column(db.Integer)
    client_ip = db.Column(db.String)
    request = db.Column(db.String)
    response = db.Column(db.String)
    subDomain = db.Column(db.String)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, protocol, interactionString, time, client_ip, request, response, subDomain):
        self.protocol = protocol
        self.interactionString = interactionString
        self.time = time
        self.client_ip = client_ip
        self.request = request
        self.response = response
        self.subDomain = subDomain

class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    
    callbacks = db.relationship("Callback")
    packages = db.relationship("Package")

    def __init__(self, name, description):
        self.name = name
        self.description = description

class Package(db.Model):
    __tablename__ = "packages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    version = db.Column(db.String)
    vulnerable = db.Column(db.Boolean)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, name, version, vulnerable):
        self.name = name
        self.version = version
        self.vulnerable = vulnerable


