# models.p

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

print("models.py loaded")

class DisasterEvent(db.Model):
    print("DisasterEvent class loaded")
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<DisasterEvent {self.name}>"

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #prediction_value = db.Column(db.Float)
    event_id = db.Column(db.Integer, db.ForeignKey('disaster_event.id'))
    prediction_date = db.Column(db.DateTime, nullable=False)
    prediction_details = db.Column(db.Text, nullable=True)
    #event = db.relationship('DisasterEvent', backref=db.backref('predictions', lazy=True))

    
    def __repr__(self):
        return f"<Prediction {self.id}>"
    
    
# UserSettings model ko yahan add karein
#class UserSettings(db.Model):
 #   id = db.Column(db.Integer, primary_key=True)
  #  username = db.Column(db.String(80), unique=True, nullable=False)
   # email = db.Column(db.String(120), unique=True, nullable=False)
    #alert_threshold = db.Column(db.String(20), nullable=False)
    #email_notifications = db.Column(db.Boolean, default=False)
#
 #   def __repr__(self):
  #      return f'<UserSettings {self.username}>'
