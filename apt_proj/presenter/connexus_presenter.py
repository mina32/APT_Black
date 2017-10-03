#!/usr/bin/env python

# [START imports]
import os
import urllib
import logging
import time

from pprint import pprint

from google.appengine.api import users
from google.appengine.api.users import User
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.db import Key
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers

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
                email=current_user.email()
            )
        )
        owned_streams = owned_query.fetch()

        subscribed_query = Stream.query(
            Stream.subscribers == Person(
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
        #logging.info([ndb.Key(Stream, k) for k in list_of_key_strings])
        ndb.delete_multi([ndb.Key(Stream, int(k)) for k in list_of_key_strings])
        #XXX: We should not hard-code sleep time
        time.sleep(1)
        self.redirect('/manage')
# [END DeleteStream]

# [START SubscribeStream]
class SubscribeStream(webapp2.RequestHandler):
    
    def post(self, stream_key_str):
        current_user = users.get_current_user()
        stream_key = ndb.Key(urlsafe=stream_key_str)
        stream_obj = stream_key.get()
        current_person = Person(
            email = current_user.email()
        )
        if len(stream_obj.subscribers):
            stream_obj.subscribers = stream_obj.subscribers.append(current_person)
        else:
            stream_obj.subscribers = [current_person]
        stream_obj.put()
        self.redirect('/view/' + stream_key_str)
# [END SubscribeStream]


# [START UnsubscribeStream]
class UnsubscribeStream(webapp2.RequestHandler):
    
    def post(self):
        list_of_key_strings = self.request.get_all("unsubscribe")
        list_of_entities = ndb.get_multi([ndb.Key(Stream, int(k)) for k in list_of_key_strings])
        current_user = users.get_current_user()
        current_person = Person(
            email=current_user.email()
        )
        logging.info(list_of_entities)
        for e in list_of_entities:
            e.subscribers.remove(current_person)
        logging.info(list_of_entities)
        ndb.put_multi(list_of_entities)
        #XXX: We should not hard-code sleep time
        time.sleep(1)
        self.redirect('/manage')
# [END UnsubscribeStream]


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
                email=u_email
        )
        # Process subscribers
        subscriber_emails = self.request.get('subscribers').split(",")
        #TODO: handle email
        subscribers = []
        for e in subscriber_emails:
            s_person = Person(
                email = e
            )
            subscribers.append(s_person)
        logging.info(subscribers)

        # Process tags
        raw_tags = self.request.get('tags')
        #TODO: Decide if we want to go back to repeated
        #tags = raw_tags.replace(' ','').split(r',')
        tags = raw_tags
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
class ViewSinglePage(webapp2.RequestHandler):
    
    def get(self, stream_key_str):
        current_user = users.get_current_user()
        stream_key = ndb.Key(urlsafe=stream_key_str)
        stream_obj = stream_key.get()
        stream_obj.views = stream_obj.views + 1
        stream_obj.put()
        media_items = stream_obj.media_items

        template_values = {
            'navigation': NAV_LINKS,
            'user': current_user,
	    'page_title': "connexus",
	    'page_header': "Connex.us",
            'stream_key': stream_key_str,
            'stream_obj': stream_obj,
            'media_items': media_items,
        }

        template = JINJA_ENVIRONMENT.get_template('view_single_stream.html')
        self.response.write(template.render(template_values))
# [END ViewSinglePage]

import cgi

# [START PostMedia]
class PostMedia(blobstore_handlers.BlobstoreUploadHandler):

    def post(self, stream_key_str):
        current_user = users.get_current_user()
        current_user = Person(
                email = current_user.email()
        )
        try:
            # TODO: Brice replace this with your backend. 
            #       This Does not work
            upload = self.get_uploads()[0]
            logging.info(upload)
            user_photo = Media(
                uploaded_by = current_user,
                content = upload.key())
            user_photo.put()
            stream_key = ndb.Key(urlsafe=stream_key_str)
            stream_obj = stream_key.get()
            stream_obj.media_items.append(user_photo)
            stream_obj.put()

            self.redirect('/view/%s' % stream_key_str)

        except:
            self.error(500)
# [END PostMedia]

# [START ViewAllPage]
# [END ViewAllPage]

# [START SearchPage]
class SearchPage(webapp2.RequestHandler):
    #in progress... 
    def get(self):
        current_user = users.get_current_user()
        # TODO: use Search API
        search_results = []
        options = search.QueryOptions(
		limit=100,
		returned_fields=['stream_name', 'id'])

	query_string = self.request.get('query')
        logging.info(query_string)
	query = search.Query(query_string=query_string) #, options=options)
        logging.info(pprint(search.Index('api-stream')))
	search_results = search.Index('api-stream').search(query)
        logging.info(pprint(search_results))

        template_values = {
            'navigation': NAV_LINKS,
            'user': current_user,
	    'page_title': "connexus",
	    'page_header': "Connex.us",
            'query': self.request.get('query'),
            'search_results': search_results,
            'results_length': 0, #len(search_results),
        }
        template = JINJA_ENVIRONMENT.get_template('search_streams.html')
        self.response.write(template.render(template_values))
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
    ('/unsub_stream', UnsubscribeStream),
    ('/sub_stream/(.+)', SubscribeStream),
    ('/view/(.+)',ViewSinglePage),
    ('/post_media/(.+)', PostMedia),
    ('/search', SearchPage),
    #('/view',ViewAllPage),
    ('/trending',TrendingPage),
    ('/error',ErrorPage),
], debug=True)
# [END app]
