#!/usr/bin/env python

# [START imports]
import os
import urllib
import logging

from pprint import pprint

from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.db import Key

import jinja2
import webapp2

from models.connexus_models import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

NAV_LINKS = [
    {"label": "Manage", "link": "/manage"},
    {"label": "Create", "link": "/create"},
    {"label": "View", "link": "/view"},
    {"label": "Search", "link": "/search"},
    {"label": "Trending", "link": "/trending"},
    {"label": "Social", "link": "/social"},
]
        
# [START ManagePage]
class ManagePage(webapp2.RequestHandler):
    
    def get(self):
        current_user = users.get_current_user()

        owned_query = Stream.query(
            Stream.owner == Person(
                identity=current_user.user_id(),                
                email=current_user.email()
            )
        )
        owned_streams = owned_query.fetch()

        subscribed_query = Stream.query(
            Stream.subscribers == Person(
                identity=current_user.user_id(),                
                email=current_user.email()
            )
        )
        subscribed_streams = subscribed_query.fetch()


        template_values = {
            'navigation': NAV_LINKS,
            'user': current_user,
	    'page_title': "connexus",
	    'page_header': "Connex.us",
            'subscribed_streams': subscribed_streams,
            'owned_streams': owned_streams,
        }

        template = JINJA_ENVIRONMENT.get_template('manage_streams.html')
        self.response.write(template.render(template_values))
# [END ManagePage]

# [START DeleteStream]
class DeleteStream(webapp2.RequestHandler):
    
    def post(self):
        list_of_key_strings = self.request.get_all("del")
        logging.info(list_of_key_strings)
        #TODO: figure out how to get keys from ID :(
        list_of_keys = []
        ndb.delete_multi(list_of_keys)
        self.redirect('/manage')
# [END DeleteStream]

# [START CreatePage]
class CreatePage(webapp2.RequestHandler):
    
    def get(self):
        current_user = users.get_current_user()
        submit_url = "/manage" 

        template_values = {
            'navigation': NAV_LINKS,
            'user': current_user,
	    'page_title': "connexus",
	    'page_header': "Connex.us",
            'stream_name_label': Stream.stream_name._verbose_name,
            'subscriber_label': Stream.subscribers._verbose_name,
            'tag_label': Stream.tags._verbose_name,
            'submit_label': "Create Stream",
            'cover_image_label': Stream.cover_image._verbose_name,
            'url': submit_url,
        }

        template = JINJA_ENVIRONMENT.get_template('create_stream.html')
        self.response.write(template.render(template_values))
# [END CreatePage]


# [START CreatePost]
class CreatePost(webapp2.RequestHandler):

    def post(self):
        current_user = users.get_current_user()
        u_id = current_user.user_id()
        u_email = current_user.email()
        owner = Person(
                identity=u_id,
                email=u_email
        )
        # Process subscribers
        subscriber_emails = self.request.get('subscribers')
        #TODO: handle email & user mapping 
        subscribers = []

        # Process tags
        raw_tags = self.request.get('tags')
        tags = raw_tags.replace(' ','').split(r',')
        s = Stream(
                stream_name=self.request.get('stream_name'),
                owner=owner,
                cover_image=self.request.get('cover_image'),
                subscribers=subscribers,
                tags=tags,
                views=0,
        )
        s.put()
        self.redirect('/manage')
# [END CreatePost]

# [START ViewSinglePage]
# [END ViewSinglePage]

# [START ViewAllPage]
# [END ViewAllPage]

# [START SearchPage]
# [END SearchPage]

# [START TrendingPage]
class TrendingPage(webapp2.RequestHandler):
    #in progress... need to get images/stream
    def get(self):
        current_user = users.get_current_user()
        trend_streams = Stream.query().order(Stream.views).fetch(3)
        template_values = {
            'navigation': NAV_LINKS,
            'user': current_user,
	    'page_title': "connexus",
	    'page_header': "Connex.us",
            'top_streams':trend_streams
        }
        template = JINJA_ENVIRONMENT.get_template('trending_stream.html')
        self.response.write(template.render(template_values))
        
# [END TrendingPage]

# [START ErrorPage]
class ErrorPage(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('error.html')
        self.response.write(template.render())
# [END ErrorPage]



# [START app]
# TODO: uncomment as pages get developed
app = webapp2.WSGIApplication([
    ('/', CreatePage),
    ('/create', CreatePage),
    ('/create_post', CreatePost),
    ('/manage', ManagePage),
    ('/delete_stream', DeleteStream),
    #('/view/<>',ViewSinglePage),
    #('/view',ViewAllPage),
    ('/trending',TrendingPage),
    ('/error',ErrorPage),
], debug=True)
# [END app]
