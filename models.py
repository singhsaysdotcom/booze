from google.appengine.ext import db

class Index(db.Model):
  name = db.StringProperty()
