#!/usr/bin/env python

# [START imports]
import os
import urllib
import logging
import time

import jinja2
import webapp2

try:
    from pprint import pprint
    from google.appengine.api import users
    from google.appengine.ext import ndb
    from google.appengine.ext.db import Key
    from google.appengine.ext import blobstore
    from google.appengine.api import images
    from google.appengine.ext.webapp import blobstore_handlers
    from models.connexus_models import *
    from models.image_store import ImageStore
except ImportError:
    raise("Import Error")

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

def check_auth(uri):
    """
        Checks if the current user is authenticated
        Returns the current user, the url and the url_link_text
    """
    current_user = users.get_current_user()
    if current_user:
        auth_url = users.create_logout_url(uri)
        url_link_text = 'Logout'
    else:
        auth_url = users.create_login_url(uri)
        url_link_text = 'Login'
    return current_user, auth_url, url_link_text


# [START UserAuthentication]
class Auth(webapp2.RequestHandler):

    def get(self):
        logging.info("-------------------")
        submit_url = "/manage"
        current_user, auth_url, url_link_text = check_auth(self.request.uri)

        if current_user:
            # Proceed to Create stream page if user exists
            template_values = {
                'navigation': NAV_LINKS,
                'user': current_user,
                'page_header': "Connex.us",
                'stream_name_label': Stream.stream_name._verbose_name,
                'subscriber_label': Stream.subscribers._verbose_name,
                'tag_label': Stream.tags._verbose_name,
                'submit_label': "Create Stream",
                'cover_image_label': Stream.cover_image._verbose_name,
                'auth_url': auth_url,
                'url_link_text': url_link_text,
                'url': submit_url,
            }

            template = JINJA_ENVIRONMENT.get_template('create_stream.html')
            self.response.write(template.render(template_values))
        else:
            # Return the login page
            template_values = {
                'page_header': "Welcome to Connexus!",
                'auth_url': auth_url,
                'url_link_text': url_link_text,
            }

            template = JINJA_ENVIRONMENT.get_template('auth.html')
            self.response.write(template.render(template_values))

    def post(self):
        submit_url = "/manage"

        current_user, auth_url, url_link_text = check_auth(self.request.uri)

        tp = users.User(self.request.get("userEmail"))
        logging.info(tp.user_id())
        # TODO Use this userEmail and Password to sign in
        logging.info(self.request.get("userEmail"))
        logging.info(self.request.get("userPassword"))

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
            'auth_url': auth_url,
            'url_link_text': url_link_text,
            'url': submit_url,
        }

        template = JINJA_ENVIRONMENT.get_template('create_stream.html')
        self.response.write(template.render(template_values))
# [END UserAuthentication]

# [START CreatePage]
class CreatePage(webapp2.RequestHandler):
    def get(self):
        submit_url = "/manage"
        current_user, auth_url, url_link_text = check_auth(self.request.uri)

        if current_user is None:
            self.redirect("/auth")
            return

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
            'auth_url': auth_url,
            'url_link_text': url_link_text,
            'url': submit_url,
        }

        template = JINJA_ENVIRONMENT.get_template('create_stream.html')
        self.response.write(template.render(template_values))

    def post(self):
        current_user, auth_url, url_link_text = check_auth(self.request.uri)

        if current_user is None:
            self.redirect("/auth")
            return

        u_id = current_user.user_id()
        u_email = current_user.email()
        owner = Person(
            identity=u_id,
            email=u_email
        )
        # Process subscribers
        subscriber_emails = self.request.get('subscribers')
        # TODO: handle email & user mapping
        subscribers = []

        # Process tags
        raw_tags = self.request.get('tags')
        tags = raw_tags.replace(' ', '').split(r',')
        s = Stream(
            stream_name=self.request.get('stream_name'),
            owner=owner,
            cover_image=self.request.get('cover_image'),
            subscribers=subscribers,
            tags=tags,
            views=0,
        )
        s = s.put()
        self.redirect('/manage')
# [END CreatePage]


# [START ManagePage]
class ManagePage(webapp2.RequestHandler):
    
    def get(self):
        current_user, auth_url, url_link_text = check_auth(self.request.uri)

        if current_user:
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
                'auth_url': auth_url,
                'url_link_text': url_link_text,
            }
            template = JINJA_ENVIRONMENT.get_template('manage_streams.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect("/auth")
# [END ManagePage]

# [START DeleteStream]
class DeleteStream(webapp2.RequestHandler):
    
    def post(self):
        current_user, auth_url, url_link_text = check_auth(self.request.uri)
        list_of_key_strings = self.request.get_all("del")
        #logging.info([ndb.Key(Stream, k) for k in list_of_key_strings])
        ndb.delete_multi([ndb.Key(Stream, int(k)) for k in list_of_key_strings])
        #XXX: We should not hard-code sleep time
        time.sleep(1)
        self.redirect('/manage')
# [END DeleteStream]

# [START UnsubscribeStream]
class UnsubscribeStream(webapp2.RequestHandler):
    
    def post(self):
        list_of_key_strings = self.request.get_all("unsubscribe")
        list_of_entities = ndb.get_multi([ndb.Key(Stream, k) for k in list_of_key_strings])
        current_user, auth_url, url_link_text = check_auth(self.request.uri)

        curentUser = Person(
            identity=current_user.user_id(),                
            email=current_user.email()
        )
        logging.info(list_of_entities)
        for e in list_of_entities:
            e.subscribers.remove(currentUser)
        logging.info(list_of_entities)
        ndb.put_multi([ndb.Key(Stream, int(k)) for k in list_of_entities])
        #XXX: We should not hard-code sleep time
        time.sleep(1)
        self.redirect('/manage')
# [END UnsubscribeStream]

# [START ViewSinglePage]
class ViewSinglePage(webapp2.RequestHandler):
    
    def get(self, stream_key_str):
        current_user, auth_url, url_link_text = check_auth(self.request.uri)

        if current_user is None:
            self.redirect("/auth")
            return

        try:

            stream_key = ndb.Key(urlsafe=stream_key_str)
            stream_obj = stream_key.get()
            stream_obj.views = stream_obj.views + 1
            stream_obj.put()

            media_items = stream_obj.media_items
            logging.info(media_items)
            template_values = {
                'navigation': NAV_LINKS,
                'user': current_user,
                'page_title': "connexus",
                'page_header': "Connex.us",
                'stream_key': stream_key_str,
                'stream_obj': stream_obj,
                'media_items': media_items,
                'auth_url': auth_url,
                'url_link_text': url_link_text,
            }
            template = JINJA_ENVIRONMENT.get_template('view_single_stream.html')
            self.response.write(template.render(template_values))
        except:
            self.redirect('/error')
# [END ViewSinglePage]

# [START PostMedia]
class PostMedia(blobstore_handlers.BlobstoreUploadHandler):

    def post(self, stream_key_str):
        current_user, auth_url, url_link_text = check_auth(self.request.uri)

        if current_user is None:
            self.redirect('/auth')
            return

        current_user = Person( identity = current_user.user_id(), email = current_user.email() )
        try:
            fieldStorage = self.request.POST["uploadImage"]
            inputImage = self.request.get("uploadImage")
            uploadComment = self.request.get("uploadComment")
            content_type = fieldStorage.type
            filename = fieldStorage.filename

            imageStore = ImageStore()
            imageKey   = "{}-{}".format(stream_key_str, filename)
            imageUrl   = imageStore.store_file(imageKey, inputImage, content_type)

            user_photo = Media(uploaded_by=current_user, content_url=imageUrl, comment = uploadComment)

            # Update stream
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

        template_values = {
            'navigation': NAV_LINKS,
            'user': current_user,
            'page_title': "connexus",
            'page_header': "Connex.us",
            'query': self.request.get('query'),
            'search_results': search_results,
            'results_length': len(search_results),
        }
        template = JINJA_ENVIRONMENT.get_template('search_streams.html')
        self.response.write(template.render(template_values))
# [END SearchPage]

# [START TrendingPage]
class TrendingPage(webapp2.RequestHandler):
    #in progress... need to get images/stream
    def get(self):
        current_user, auth_url, url_link_text = check_auth(self.request.uri)
        trend_streams = Stream.query().order(Stream.views).fetch(3)
        template_values = {
            'navigation': NAV_LINKS,
            'user': current_user,
            'page_title': "connexus",
            'page_header': "Connex.us",
            'top_streams':trend_streams,
            'auth_url': auth_url,
            'url_link_text': url_link_text,
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
    ('/', Auth),
    ('/auth', Auth),
    ('/create', CreatePage),
    ('/manage', ManagePage),
    ('/delete_stream', DeleteStream),
    ('/view/(.+)',ViewSinglePage),
    ('/post_media/(.+)', PostMedia),
    ('/search', SearchPage),
    #('/view',ViewAllPage),
    ('/trending',TrendingPage),
    ('/error',ErrorPage),
], debug=True)
# [END app]
