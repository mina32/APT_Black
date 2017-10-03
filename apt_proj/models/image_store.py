#!/usr/bin/env python

from __future__ import absolute_import

# [START imports]
import os
import sys
# import jinja2
# import urllib
# import webapp2
import logging

try:
    logging.info("a1")
    import models.lib.cloudstorage as gcs
    logging.info("a")
    from google.appengine.api import app_identity       # Gets the default bucket for us
    logging.info("b")
except ImportError:
    # raise("Import error in image_store.py")
    logging.info("0000000000000000000000000000000")
    exit(1)
# [END imports]

class ImageStorage(object):
    def __init__(self):
        self.gcsHandle = gcs
        self.bucketName = os.environ.get('BUCKET_NAME',
                                          app_identity.get_default_gcs_bucket_name())
        self.bucket = '/' + self.bucketName

    # [START store_file]
    def store_file(self, filename, content, content_type='image/png'):
        write_retry_params = self.gcsHandle.RetryParams(backoff_factor=1.1)

        # Open a file
        gcsFile = self.gcsHandle.open(filename, 'w', content_type=content_type,
                                      options={'x-goog-acl': 'private'}, retry_params=write_retry_params)

        # Write to the file
        gcsFile.write(content)
        gcsFile.close()
    # [END store_file]

    # [START retrieve_file]
    def retrieve_file(self, filename):
        storedPath = self.bucket + "/" + filename
        # Open file
        logging.info(storedPath)
        gcsFile = self.gcsHandle.open(storedPath)

        # Read the file's content
        imageBlog = gcsFile.read(-1)
        gcsFile.close()
        return imageBlog
    # [END retrieve_file]

    # [START delete_file]
    def delete_files(self, filenames=[]):
        if not isinstance(filenames, list):
            raise("Supply a list of files to delete")

        for file in filenames:
            try:
                self.gcsHandle.delete(file)
            except gcs.NotFoundError:
                pass
    # [END delete_file]

    # [START list_files]
    def list_files(self, pattern='/'):
        if not isinstance(pattern, str):
            raise ("Supply a matching pattern as a string")

        newPattern = self.bucket + pattern
        stats = gcs.listbucket(newPattern)

        return [(stat.filename, stat.etag, stat.st_size, stat.st_ctime) for stat in stats]
    # [END list_files]