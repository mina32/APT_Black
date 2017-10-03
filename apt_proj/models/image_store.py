#!/usr/bin/env python

from __future__ import absolute_import

# [START imports]
import os
import sys

try:
    import models.lib.cloudstorage as gcs
    from google.appengine.api import app_identity       # Gets the default bucket for us
except ImportError:
    raise("Unable to import GCS")
# [END imports]

class ImageStore(object):
    def __init__(self):
        self.gcsHandle = gcs
        self.bucketName = os.environ.get('BUCKET_NAME',
                                          app_identity.get_default_gcs_bucket_name())
        self.bucket = '/' + self.bucketName

    # [START store_file]
    def store_file(self, filename, content, content_type='image/png'):
        storedPath = self.bucket + "/" + filename + ".png"
        write_retry_params = self.gcsHandle.RetryParams(backoff_factor=1.1)

        # Open a file
        gcsFile = self.gcsHandle.open(storedPath, 'w', content_type=content_type,
                                      options={'x-goog-acl': 'authenticated-read'}, retry_params=write_retry_params)

        # Write to the file
        gcsFile.write(content)
        gcsFile.close()
    # [END store_file]

    # [START retrieve_file]
    def retrieve_file(self, filename):
        storedPath = self.bucket + "/" + filename
        # Open file
        gcsFile = self.gcsHandle.open(storedPath)

        # Read the file's content
        imageBlog = gcsFile.read(-1)
        gcsFile.close()
        return imageBlog
    # [END retrieve_file]

    # [START delete_file]
    def delete_files(self, filenames):
        if not isinstance(filenames, list):
            raise("Supply a list of files to delete")

        for file in filenames:
            try:
                storedFile = self.bucket + "/" + file
                self.gcsHandle.delete(storedFile)
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