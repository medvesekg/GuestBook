from google.appengine.ext import ndb

class Post(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    message = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)