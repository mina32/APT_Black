#!/usr/bin/env python

# [START imports]
import os
import urllib
import logging
import time
import json
import random

import jinja2
import webapp2

try:
    from pprint import pprint
    from math import sin, cos, sqrt, atan2, radians
    from google.appengine.api import users
    from google.appengine.ext import ndb
    from google.appengine.ext.db import Key
    from google.appengine.ext import blobstore
    from google.appengine.api import images
    from google.appengine.ext.webapp import blobstore_handlers
    from models.connexus_models import *
    from models.image_store import ImageStore
    from google.appengine.api import app_identity
    from google.appengine.api import mail
    from datetime import datetime
except ImportError:
    raise("Import Error")

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

REPORT_RATE_MINUTES = "0"
LAST_REPORT = None
SECS_PER_HOUR = 3600

NAV_LINKS = [
    {"label": "Manage", "link": "/manage"},
    {"label": "Create", "link": "/create"},
    {"label": "View", "link": "/view"},
    {"label": "Search", "link": "/search"},
    {"label": "Trending", "link": "/trending"},
    {"label": "Social", "link": "/social"},
]

def check_auth(request, isAppRequest=False):
    """
        Checks if the current user is authenticated
        Returns the current user, the url and the url_link_text
    """
    app_connection = False;

    if isAppRequest:
        app_connection = True
        current_user = Person(email=request.get("userEmail"))
        return current_user, "", "", app_connection

    current_user = users.get_current_user()
    logging.info(current_user)
    if current_user:
        auth_url = users.create_logout_url(request.uri)
        url_link_text = 'Logout'
    else:
        auth_url = users.create_login_url(request.uri)
        url_link_text = 'Login'
    return current_user, auth_url, url_link_text, app_connection


# [START UserAuthentication]
class Auth(webapp2.RequestHandler):

    def get(self):
        submit_url = "/manage"
        current_user, auth_url, url_link_text, app_connection = check_auth(self.request)

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

        current_user, auth_url, url_link_text, app_connection = check_auth(self.request)

        tp = users.User(self.request.get("userEmail"))
        # TODO Use this userEmail and Password to sign in

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
        current_user, auth_url, url_link_text, app_connection = check_auth(self.request)

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
        current_user, auth_url, url_link_text, app_connection = check_auth(self.request)

        if current_user is None:
            self.redirect("/auth")
            return
        # Check name uniqueness
        name_query = Stream.query(
            Stream.stream_name == self.request.get('stream_name')
        )
        query_results = name_query.fetch()
        if (len(query_results) > 0):
            return self.redirect('/error')

        u_id = current_user.user_id()
        u_email = current_user.email()
        owner = Person(email=u_email)
        
        # Process subscribers
        subscriber_emails = self.request.get('subscribers').split(",")
        
        subscribers = []
        for e in subscriber_emails:
            if len(e):
                s_person = Person(email = e)
                subscribers.append(s_person)
        

        # Process tags
        raw_tags = self.request.get('tags')
        tags = raw_tags
                
        s = Stream(
            stream_name=self.request.get('stream_name'),
            owner=owner,
            cover_image=self.request.get('cover_image'),
            subscribers=subscribers,
            tags=tags,
            views=0,
        )

        s_key = s.put()
        #Subscriber Emails
        for e in subscriber_emails:
            if len(e):
                logging.info(e)
                mail.send_mail(sender=u_email,
                    to="<" + e + ">",
                    subject="New subscription alert",
                    body="You have been added as a subscriber to the stream at " + 
                        app_identity.get_application_id() + ".appspot.com/view/" + s_key.urlsafe()
                        + ".\nMessage from stream creator: " + self.request.get('subscribers_msg') 
                )

        fields = [
            search.TextField(name = 'stream_name', value = s.stream_name),
            search.TextField(name = 'tags', value = s.tags),
        ]
        
        d = search.Document(doc_id = str(s_key.urlsafe()), fields = fields)
        try:
            add_result = search.Index('api-stream').put(d)
        except search.Error:
            logging.exception("Error adding document:")

        # Now create SearchableString objects
        search_strings = s.stream_name + " " + s.tags.replace(","," ")
        search_strings_list = search_strings.split()
        for search_str in search_strings_list:
            matching_query = SearchableString.query(
            SearchableString.search_tag == search_str,
            )
            matches = matching_query.fetch(1)
            if (len(matches) == 0):
                search_string = SearchableString(
                    search_tag = search_str.lower()
                )
                search_string.put()
        self.redirect('/manage')
# [END CreatePage]

# [START ManagePage]
class ManagePage(webapp2.RequestHandler):
    
    def get(self):
        current_user, auth_url, url_link_text, app_connection = check_auth(self.request)

        if current_user:
            owned_query = Stream.query(
                Stream.owner == Person(email=current_user.email())
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
        current_user, auth_url, url_link_text, app_connection = check_auth(self.request)
        list_of_key_strings = self.request.get_all("del")
        for k in list_of_key_strings:
             search.Index('api-stream').delete(ndb.Key(Stream, int(k)).urlsafe())
        ndb.delete_multi([ndb.Key(Stream, int(k)) for k in list_of_key_strings])
        #XXX: We should not hard-code sleep time
        time.sleep(1)
        self.redirect('/manage')
# [END DeleteStream]

# [START SubscribeStream]
class SubscribeStream(webapp2.RequestHandler):
    
    def post(self, stream_key_str):
        current_user, auth_url, url_link_text, app_connection = check_auth(self.request)

        if current_user is None:
            self.redirect('/view/' + stream_key_str + "?auth_status_message=User is not logged in.")
            return

        stream_key = ndb.Key(urlsafe=stream_key_str)
        stream_obj = stream_key.get()
        current_person = Person(
            email = current_user.email()
        )
        if len(list(stream_obj.subscribers)):
            subscribers = [p for p in stream_obj.subscribers]
            subscribers.append(current_person)
            stream_obj.subscribers = subscribers
        else:
            subscribers = []
            subscribers.append(current_person)
            stream_obj.subscribers = subscribers
        stream_obj.put()
        self.redirect('/view/' + stream_key_str)
# [END SubscribeStream]

# [START UnsubscribeStream]
class UnsubscribeStream(webapp2.RequestHandler):
    
    def post(self):
        list_of_key_strings = self.request.get_all("unsubscribe")
        list_of_entities = ndb.get_multi([ndb.Key(Stream, int(k)) for k in list_of_key_strings])
        current_user, auth_url, url_link_text, app_connection = check_auth(self.request)

        if current_user is None:
            self.redirect('/auth')
            return

        current_person = Person(
            email=current_user.email()
        )
        for e in list_of_entities:
            e.subscribers.remove(current_person)
        ndb.put_multi(list_of_entities)
        #XXX: We should not hard-code sleep time
        time.sleep(1)
        self.redirect('/manage')
# [END UnsubscribeStream]

# [START ViewSinglePage]
class ViewSinglePage(webapp2.RequestHandler):
    
    def get(self, stream_key_str):
        current_user, auth_url, url_link_text, app_connection = check_auth(self.request)

        try:
            stream_key = ndb.Key(urlsafe=stream_key_str)
            stream_obj = stream_key.get()
            stream_obj.views = stream_obj.views + 1
            while len(stream_obj.recent_views) > 0 and (datetime.now() - stream_obj.recent_views[0]).seconds > 3600:
                del stream_obj.recent_views[0]
            stream_obj.recent_views.append(datetime.now())
            stream_obj.put()

            media_items = stream_obj.media_items
            length = len(media_items)
            template_values = {
                'navigation': NAV_LINKS,
                'user': current_user,
                'page_title': "connexus",
                'page_header': "Connex.us",
                'stream_key': stream_key_str,
                'stream_obj': stream_obj,
                'media_items': media_items,
                'length': length,
                'auth_url': auth_url,
                'url_link_text': url_link_text,
                "auth_status_message": self.request.get('auth_status_message'),
            }
            template = JINJA_ENVIRONMENT.get_template('view_single_stream.html')
            self.response.write(template.render(template_values))
        except:
            self.redirect('/error')
# [END ViewSinglePage]

# [START ViewAllPage]
class ViewAllPage(webapp2.RequestHandler):
    
    def get(self):
        try:
            current_user, auth_url, url_link_text, app_connection = check_auth(self.request)
            all_streams = Stream.query().fetch()
            template_values = {
                'navigation': NAV_LINKS,
                'user': current_user,
                'page_title': "connexus",
                'page_header': "Connex.us",
                'streams': all_streams,
                'auth_url': auth_url,
                'url_link_text': url_link_text,
            }
            template = JINJA_ENVIRONMENT.get_template('view_all_streams.html')
            self.response.write(template.render(template_values))
        except:
            self.redirect('/error')
# [END ViewAllPage]


# [START PostMedia]
class PostMedia(blobstore_handlers.BlobstoreUploadHandler):

    def post(self, stream_key_str):
        current_user, auth_url, url_link_text, app_connection = check_auth(self.request)

        if current_user is None:
            self.redirect('/auth')
            return

        current_user = Person( email = current_user.email() )
        try:
            fieldStorage = self.request.POST["uploadImage"]
            inputImage = self.request.get("uploadImage")
            uploadComment = self.request.get("uploadComment")
            content_type = fieldStorage.type
            filename = fieldStorage.filename

            imageStore = ImageStore()
            imageKey   = "{}-{}".format(stream_key_str, filename)
            imageUrl   = imageStore.store_file(imageKey, inputImage, content_type)

            # GeoView -- web view sets random points.
            lat = - 60.4301233 + 89.4245046 * random.random()
            lon = - 287.057815 + 185.035715 * random.random()

            user_photo = Media(
                    uploaded_by=current_user,
                    content_url=imageUrl,
                    comment = uploadComment,
                    location=ndb.GeoPt(lat,lon),
            )

            # Update stream
            stream_key = ndb.Key(urlsafe=stream_key_str)
            stream_obj = stream_key.get()
            stream_obj.media_items.append(user_photo)
            stream_obj.put()
            self.redirect('/view/%s' % stream_key_str)
        except:
            self.error(500)
# [END PostMedia]


# [START SearchPage]
class SearchPage(webapp2.RequestHandler):
    def get(self):
        current_user, auth_url, url_link_text, app_connection = check_auth(self.request)
        query_string = self.request.get('query')
        query = search.Query(query_string=query_string) #, options=options)
        search_results = search.Index('api-stream').search(query)
        search_result_keys = [d.doc_id for d in search_results.results]
        search_result_objs = [ndb.Key(urlsafe=k).get() for k in search_result_keys]

        template_values = {
            'navigation': NAV_LINKS,
            'user': current_user,
            'page_title': "connexus",
            'page_header': "Connex.us",
            'query': self.request.get('query'),
            'search_results': search_result_objs,
            'results_length': len(search_result_objs),
            'auth_url': auth_url,
            'url_link_text': url_link_text,
        }
        template = JINJA_ENVIRONMENT.get_template('search_streams.html')
        self.response.write(template.render(template_values))
# [END SearchPage]

# [START SearchOptions]
class SearchOptions(webapp2.RequestHandler):
    def get(self):
        query_string = self.request.get('query').lower()
        query_limit = query_string[:-1] + chr(ord(query_string[-1]) + 1)
        matching_query = SearchableString.query(
            SearchableString.search_tag >= query_string,
            SearchableString.search_tag < query_limit,
        )
        matches = matching_query.fetch(20)
        self.response.out.write(json.dumps([i.search_tag for i in matches]))
# [END SearchOptions]


# [START TrendingPage]
class TrendingPage(webapp2.RequestHandler):

    def get(self):
        
        current_user, auth_url, url_link_text, app_connection = check_auth(self.request)
        
        all_streams = Stream.query().fetch()
        sorted_streams = sorted(all_streams, key=lambda s: len(s.recent_views),
                                reverse=True)
        size = 3 
        if (len(sorted_streams) < 3):
            size = len(sorted_streams)

        checked = [""] * 4
        cur_rate = REPORT_RATE_MINUTES

        if cur_rate:
            if cur_rate == '0':
                checked[0] = "checked=checked"
            elif cur_rate == '5':
                checked[1] = "checked=checked"
            if cur_rate == '60':
                checked[2] = "checked=checked"
            elif cur_rate == '1440':
                checked[3] = "checked=checked"
        else:
            checked[0] = "checked=checked"

        template_values = {
            'navigation': NAV_LINKS,
            'user': current_user,
            'page_title': "connexus",
            'page_header': "Connex.us",
            'top_streams': sorted_streams[:size],
            'checked': checked,
            'auth_url': auth_url,
            'url_link_text': url_link_text,
        }
        template = JINJA_ENVIRONMENT.get_template('trending_stream.html')
        self.response.write(template.render(template_values))

    def post(self):
        rate = self.request.get('rate')
        global REPORT_RATE_MINUTES
        REPORT_RATE_MINUTES =rate
        self.redirect('/trending')
# [END TrendingPage]

# [START LeaderboadrCalc]
class LeaderboardCalc(webapp2.RequestHandler):

    def get(self):
        streams = Stream.query().fetch()
        now = datetime.datetime.now()
        for stream in streams:
            stream.recent_views = filter(lambda v: (now - v).seconds < SECS_PER_HOUR,
                                         stream.recent_views)
            stream.put()
            
# [START SendReport]
class SendReport(webapp2.RequestHandler):

    def get(self):
        current_user, auth_url, url_link_text, app_connection = check_auth(self.request)

        if REPORT_RATE_MINUTES == '0':
            return

        global LAST_REPORT
        if not LAST_REPORT:
            LAST_REPORT = datetime.now()
            return

        delta = (datetime.now() - LAST_REPORT).seconds
        if delta < int(REPORT_RATE_MINUTES) * 60:
            return
        LAST_REPORT = datetime.now()

        #Send Trending Info
        all_streams = Stream.query.fetch()
        sorted_streams = sorted(all_streams, key=lambda s: len(s.recent_views),
                                reverse=True)
        size = 3
        if (len(sorted_streams) < 3):
            size = len(sorted_streams)

        for i, stream in enumerate(all_streams[:size]):
            body += "%d. %s %s" % (i + 1, stream.stream_name,
                                    "from http://apt-black-app.appspot.com ")

        mail.send_mail(sender=current_user.email(),
                        to="<ee382vta@gmail.com>",
                        subject="APT-BLACK Trending Report",
                        body=body)
        return

# [END SendReport]         

# [START ErrorPage]
class ErrorPage(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('error.html')
        self.response.write(template.render())
# [END ErrorPage]

# [START SocialPage]
class SocialPage(webapp2.RequestHandler):
    
    def get(self):
        current_user, auth_url, url_link_text, app_connection = check_auth(self.request)
        template_values = {
            'navigation': NAV_LINKS,
            'user': current_user,
            'page_title': "connexus",
            'page_header': "Connex.us",
            'auth_url': auth_url,
            'url_link_text': url_link_text,
        }
        
        template = JINJA_ENVIRONMENT.get_template('social.html')
        self.response.write(template.render(template_values))
# [END SocialPage]

# [START GeoView]
class GeoView(webapp2.RequestHandler):

    def get(self, stream_key_str):
        current_user, auth_url, url_link_text, app_connection = check_auth(self.request)

        if current_user is None:
            self.redirect("/auth")
            return

        stream_key = ndb.Key(urlsafe=stream_key_str)
        stream_obj = stream_key.get()

        media_map = []
        for media_item in stream_obj.media_items:
            createTime = str(media_item.date_uploaded)[:10] + 'T' + str(media_item.date_uploaded)[11:] + 'Z'
            lat = - 60.4301233 + 89.4245046 * random.random()
            lon = - 287.057815 + 185.035715 * random.random()
            if ((media_item.location is not None) and 
                (media_item.location.lat is not None) and
                (media_item.location.lon is not None)
            ):
                lat = media_item.location.lat
                lon = media_item.location.lon
            url = media_item.content_url

            media_map.append({
                "createTime": createTime,
                "lat": lat,
                "lon": lon,
                "url": url,
            })

        template_values = {
            'navigation': NAV_LINKS,
            'user': current_user,
            'page_title': "connexus",
            'page_header': "Connex.us",
            'stream_key': stream_key_str,
            'stream_obj': stream_obj,
            'media_map': media_map,
            'auth_url': auth_url,
            'url_link_text': url_link_text,
        }
        template = JINJA_ENVIRONMENT.get_template('geo_view.html')
        self.response.write(template.render(template_values))
# [END GeoView]

# [START GeoPoints]
class GeoPoints(webapp2.RequestHandler):
    def get(self, stream_key_str):
        stream_key = ndb.Key(urlsafe=stream_key_str)
        stream_obj = stream_key.get()

        media_map = []
        for media_item in stream_obj.media_items:
            createTime = str(media_item.date_uploaded)[:10] + 'T' + str(media_item.date_uploaded)[11:] + 'Z'
            lat = - 60.4301233 + 89.4245046 * random.random()
            lon = - 287.057815 + 185.035715 * random.random()
            if ((media_item.location is not None) and 
                (media_item.location.lat is not None) and
                (media_item.location.lon is not None)
            ):
                lat = media_item.location.lat
                lon = media_item.location.lon
            url = media_item.content_url

            media_map.append({
                "createTime": createTime,
                "lat": lat,
                "lon": lon,
                "url": url,
            })
        self.response.out.write(json.dumps(media_map))
# [END GeoPoints]

# [START AppMostViewed]
class AppMostViewed(webapp2.RequestHandler):

    def get(self):
        jsonResp = {}
        try:
            all_streams = Stream.query().fetch()
            sorted_streams = sorted(all_streams, key=lambda s: s.date_last_updated, reverse=False)
            mapped = map( lambda s: {
                                        "owner": str(s.owner.email),
                                        "key_id": str(s.key.id()),
                                        "key_url": str(s.key.urlsafe()),
                                        "cover_image": str(s.cover_image),
                                        "stream_name": str(s.stream_name),
                                        "subscribers": map(lambda x : str(x.email), s.subscribers),
                                        },
                                        sorted_streams )

            jsonResp = {"all_streams": mapped}
        except:
            pass

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(str(json.dumps(jsonResp)))
# [END AppMostViewed]

# [START AppRecentSubscribed]
class AppRecentSubscribed(webapp2.RequestHandler):
    def get(self):
        jsonResp = {}
        try:
            current_user, auth_url, url_link_text, app_connection = check_auth(self.request, True)
            if current_user:
                logging.info(current_user.email);
                subscribed_query = Stream.query(Stream.subscribers == current_user)
                logging.info("===> A\n");
                logging.info("===> \n" + str(subscribed_query));
                subscribed_streams = subscribed_query.fetch()
                sorted_streams = sorted(subscribed_streams, key=lambda s: s.date_last_updated, reverse=False)
                mapped = map( lambda s: {
                                            "owner": str(s.owner.email),
                                            "key_id": str(s.key.id()),
                                            "key_url": str(s.key.urlsafe()),
                                            "cover_image": str(s.cover_image),
                                            "stream_name": str(s.stream_name)
                                        }
                                        , sorted_streams )
                jsonResp = {"subscribed_streams": mapped}
        except:
            pass

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(str(json.dumps(jsonResp)))
# [END AppRecentSubscribed]

# [START AppViewRecentImages]
class AppViewRecentImages(webapp2.RequestHandler):
    def get(self):
        jsonResp = {}
        try:
            current_user, auth_url, url_link_text, app_connection = check_auth(self.request, True)

            key_url = self.request.get("key_url")
            stream_key = ndb.Key(urlsafe=key_url)
            stream_obj = stream_key.get()
            stream_obj.views = stream_obj.views + 1
            stream_obj.recent_views.append(datetime.now())
            stream_obj.put()

            media_items = stream_obj.media_items

            sorted_streams = sorted(media_items, key=lambda s: s.date_uploaded, reverse=False)
            mapped = map( lambda m: {
                                        "image_url": str(m.content_url),
                                        "upload_date": str(m.date_uploaded),
                                    }
                                    , sorted_streams )
            jsonResp = {"media_items": mapped}
        except:
            pass

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(str(json.dumps(jsonResp)))
# [END AppViewRecentImages]

# [START AppSearchResults]
class AppSearchResults(webapp2.RequestHandler):
    def get(self):
        current_user, auth_url, url_link_text, app_connection = check_auth(self.request)
        query_string = self.request.get('query')
        query = search.Query(query_string=query_string) #, options=options)
        search_results = search.Index('api-stream').search(query)
        search_result_keys = [d.doc_id for d in search_results.results]
        search_result_objs = [ndb.Key(urlsafe=k).get() for k in search_result_keys]
        sorted_streams = sorted(search_result_objs, key=lambda s: s.date_last_updated, reverse=False)
        mapped = map( lambda s: {
                                    "owner": str(s.owner.email),
                                    "key_id": str(s.key.id()),
                                    "key_url": str(s.key.urlsafe()),
                                    "cover_image": str(s.cover_image),
                                    "stream_name": str(s.stream_name)
                                }
                                , sorted_streams )
        jsonResp = {"search_streams": mapped}
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(str(json.dumps(jsonResp)))
# [END SearchResults]

# [START AppNearbyResults]
class AppNearbyResults(webapp2.RequestHandler):
    def get_distance(self,stream_obj, lat1, lon1):
        locations = []
        if len(stream_obj.media_items):
            for media_item in stream_obj.media_items:
                if ((media_item.location is not None) and 
                    (media_item.location.lat is not None) and
                    (media_item.location.lon is not None)
                ):
                    locations.append(self.calc_distance(lat1,lon1,media_item.location.lat, media_item.location.lon))
        if len(locations):
            return sorted(locations)[0]
    
    def calc_distance(self,lat1,lon1,lat2,lon2):
        # approximate radius of earth in km
        R = 6373.0

        lat1 = radians(float(lat1))
        lon1 = radians(float(lon1))
        lat2 = radians(float(lat2))
        lon2 = radians(float(lon2))
                
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c
        return distance

    def get(self):
        current_user, auth_url, url_link_text, app_connection = check_auth(self.request)
        lat = self.request.get('lat')
        lon = self.request.get('lon')
        
        #try:
        all_streams = Stream.query().fetch()
        mapped = []
        for s in all_streams:
            item = {}
            item["distance"] = self.get_distance(s, lat, lon)
            item["owner"] = str(s.owner.email)
            item["key_id"] = str(s.key.id())
            item["key_url"] = str(s.key.urlsafe())
            item["cover_image"] = str(s.cover_image)
            item["stream_name"] = str(s.stream_name)
            item["subscribers"] = map(lambda x : str(x.email), s.subscribers)
            mapped.append(item)

        sorted_streams = sorted(mapped, key=lambda s: (s["distance"] is None, s["distance"]), reverse=False)
        jsonResp = {"streams_by_distance": sorted_streams}
        #except:
        #    pass

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(str(json.dumps(jsonResp)))
# [END NearbyResults]

# [START app]
app = webapp2.WSGIApplication([
    ('/', ViewAllPage),
    ('/auth', Auth),
    ('/create', CreatePage),
    ('/manage', ManagePage),
    ('/delete_stream', DeleteStream),
    ('/unsub_stream', UnsubscribeStream),
    ('/sub_stream/(.+)', SubscribeStream),
    ('/view/(.+)',ViewSinglePage),
    ('/post_media/(.+)', PostMedia),
    ('/search', SearchPage),
    ('/search_results', SearchOptions),
    ('/view',ViewAllPage),
    ('/trending',TrendingPage),
    ('/social',SocialPage),
    ('/error',ErrorPage),
    ('/report', SendReport),
    ('/leaderboard_calc', LeaderboardCalc),
    ('/geo/(.+)', GeoView),
    ('/get_geo_points/(.+)', GeoPoints),
    ('/androidMostViewed', AppMostViewed),
    ('/androidSubscribedStreams', AppRecentSubscribed),
    ('/androidViewImages', AppViewRecentImages),
    ('/androidSearchResults', AppSearchResults),
    ('/androidNearbyResults', AppNearbyResults),
], debug=True)
# [END app]
