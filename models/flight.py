from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///airport.sqlite"
db = SQLAlchemy(app)


class Flight(db.Model):
    id = db.Column(db.String, primary_key=True)
    destination = db.Column(db.String, nullable=False)
    carrier = db.Column(db.String, nullable=False)
    terminal = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=True)
    is_arriving = db.Column(db.Boolean, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'destination': self.destination,
            'carrier': self.carrier,
            'terminal': self.terminal,
            'status': self.status if self.status is not None else 'unknown',
            'is_arriving': self.is_arriving
        }
