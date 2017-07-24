from google.appengine.ext import ndb

class Post(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    message = ndb.StringProperty()
    deleted = ndb.BooleanProperty(default=False)
    date = ndb.DateTimeProperty(auto_now_add=True)