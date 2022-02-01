from flask_sqlalchemy import SQLAlchemy

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
    payload = db.Column(db.String)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, protocol, interactionString, time, client_ip, request, response, subDomain, payload, project_id):
        self.protocol = protocol
        self.interactionString = interactionString
        self.time = time
        self.client_ip = client_ip
        self.request = request
        self.response = response
        self.subDomain = subDomain
        self.payload = payload
        self.project_id = project_id


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    callbacks = db.relationship("Callback", lazy="dynamic")
    packages = db.relationship("Package", lazy="dynamic")

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Package(db.Model):
    __tablename__ = "packages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    version = db.Column(db.String)
    vulnerable = db.Column(db.Boolean)
    campaign_active = db.Column(db.Boolean)

    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))

    def __init__(self, name, version, vulnerable, campaing_active=False):
        self.name = name
        self.version = version
        self.vulnerable = vulnerable
        self.campaign_active = campaing_active
