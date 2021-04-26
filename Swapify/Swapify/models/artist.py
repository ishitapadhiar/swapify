from ..app import db


class Artist(db.Model):

    __tablename__ = "artist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name=None):
        self.name = name
