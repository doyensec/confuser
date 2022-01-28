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

    def __init__(self, protocol, interactionString, time, client_ip, request, response, subDomain):
        self.protocol = protocol
        self.interactionString = interactionString
        self.time = time
        self.client_ip = client_ip
        self.request = request
        self.response = response
        self.subDomain = subDomain
