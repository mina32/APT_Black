#!/usr/bin/env python

# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore 
from google.appengine.api import images
from google.appengine.api import search

import jinja2
import webapp2

from pprint import pprint

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
    email = ndb.StringProperty()

# [START Media]
class Media(ndb.Model):
    uploaded_by = ndb.StructuredProperty(Person)
    date_uploaded = ndb.DateTimeProperty(auto_now_add=True)
    comment = ndb.StringProperty(required=False, verbose_name="comment")
    content_url   = ndb.StringProperty(required=True, verbose_name="image url")
# [END Media]


# [START Stream]
class Stream(ndb.Model):
    stream_name = ndb.StringProperty(required=True, verbose_name="Name your stream") 
    owner = ndb.StructuredProperty(Person)
    media_items = ndb.StructuredProperty(Media, repeated=True)
    media_item_count = ndb.ComputedProperty(lambda x: len(x.media_items))
    cover_image = ndb.StringProperty(verbose_name="URL to cover image (Can be empty)")
    subscribers = ndb.StructuredProperty(Person, repeated=True, verbose_name="Add subscribers")
    tags = ndb.StringProperty(verbose_name="Tag your stream")
    views = ndb.IntegerProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    date_last_updated = ndb.DateTimeProperty(auto_now=True)

   # [END Stream]



