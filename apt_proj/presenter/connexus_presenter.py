#!/usr/bin/env python

# [START imports]
import os
import urllib

from pprint import pprint

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from models.connexus_models import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname('templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]


# [START ManagePage]
# [END ManagePage]

# [START CreatePage]
class CreatePage(webapp2.RequestHandler):
    
    def get(self):
        user = users.get_current_user()
        submit_url = "/manage" 

        template_values = {
            'user': user,
	    'page_title': "connexus",
	    'page_header': "Connex.us",
            'stream_name_label': Stream.stream_name._verbose_name,
            'subscriber_label': Stream.subscribers._verbose_name,
            'tag_label': Stream.tags._verbose_name,
            'submit_label': "Create Stream",
            'cover_image_label': Stream.cover_image._verbose_name,
            'url': submit_url,
        }

        template = JINJA_ENVIRONMENT.get_template('templates/create_stream.html')
        self.response.write(template.render(template_values))

    def post(self):
        pprint(self.request.data)
        # Process subscribers
        subscriber_emails = self.request.get('subscribers')
        #TODO: handle email & user mapping 
        subscribers = []

        # Process tags
        raw_tags = self.request.get('tags')
        tags = raw_tags.replace(' ','').split(r',')
        s = Stream(
                stream_name=self.request.get('name'),
                owner=user,
                cover_image=self.request.get('cover_image'),
                subscribers=subscribers,
                tags=tags,
                views=0,
        )
        s.post()
        self.redirect('/manage')
# [END CreatePage]

# [START ViewSinglePage]
# [END ViewSinglePage]

# [START ViewAllPage]
# [END ViewAllPage]

# [START SearchPage]
# [END SearchPage]

# [START TrendingPage]
# [END TrendingPage]

# [START ErrorPage]
# [END ErrorPage]



# [START app]
# TODO: uncomment as pages get developed
app = webapp2.WSGIApplication([
    ('/', CreatePage),
    ('/create', CreatePage),
    #('/manage', ManagePage),
    #('/view/<>',ViewSinglePage),
    #('/view',ViewAllPage),
    #('/trending',TrendingPage),
    #('/error',ErrorPage),
], debug=True)
# [END app]
