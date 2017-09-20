#!/usr/bin/env python

# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_STREAM_NAME = 'default_stream'


# We set a parent key on the 'Media' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def stream_key(guestbook_name=DEFAULT_STREAM_NAME):
    return ndb.Key('Stream', stream_name)


class Person(ndb.Model):
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)

# [START Media]
class Media(ndb.Model):
    #TODO: make this a filetype
    content = ndb.StringProperty(indexed=False)
    date_uploaded = ndb.DateTimeProperty(auto_now_add=True)
# [END Media]


# [START Stream]
class Stream(webapp2.RequestHandler):
    stream_name = ndb.StringProperty(required=True, verbose_name="Name your stream") 
    owner = ndb.StructuredProperty(Person)
    media_items = ndb.StructuredProperty(Media, repeated=True)
    cover_image = ndb.StringProperty(verbose_name="URL to cover image (Can be empty)")
    subscribers = ndb.StructuredProperty(Person, repeated=True, verbose_name="Add subscribers")
    tags = ndb.StringProperty(repeated=True, verbose_name="Tag your stream")
    views = ndb.IntegerProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    date_last_updated = ndb.DateTimeProperty(auto_now=True)

    
    # TODO: Does this belong in presenter? 
    #       Probs not because it applies to ALL Streams
    def post(self):
        stream_name = self.request.get('stream_name', DEFAULT_STREAM_NAME)
        media_items = Media(parent=stream_key(stream_name))

        if users.get_current_user():
            stream.owner = Owner(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())

        #greeting.content = self.request.get('content')
        #greeting.put()

        #query_params = {'stream_name': stream_name}
        #self.redirect('/?' + urllib.urlencode(query_params))
# [END Stream]



