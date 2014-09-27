#!/usr/bin/python
"""Download all the Beancount docs from Google Drive and bake a nice PDF with it.
"""
__author__ = 'Martin Blais <blais@furius.ca>'

import argparse
import urllib
import os
from os import path
from pprint import pprint as pp

from oauth2client import tools
import oauth2client.client
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

import httplib2
import googleapiclient.discovery


def get_authenticated_http(scope, storage_filename, opts):
    """Authenticate via oauth2 and store to a filename.
    If credentials are already available in the storage filename, this does not
    need user interaction; otherwise, this opens up a browser window to accept
    access.

    Args:
      scope: A string, the scope to get credentials for.
      storage_filename: A string, a path to the filename where to cache the
        credentials between runs.
      opts: An argparse option values object, as retrurned by parse_args().
    Returns:
      An authenticated http client object, from which you can use the Google APIs.
    """

    if 1:
        # With secrets stored in a file.
        secrets_filename = os.environ['GOOGLE_APIS']
        flow = oauth2client.client.flow_from_clientsecrets(secrets_filename, scope)
        flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN

        # Secrets file contents look like this:
        #
        # {"installed":
        #  {"client_id": ".....",
        #   "client_secret": ".....",
        #   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        #   "token_uri": "https://accounts.google.com/o/oauth2/token",
        #   "client_email": "",
        #   "redirect_uris": ["urn: ietf: wg: oauth: 2.0: oob", "oob"],
        #   "client_x509_cert_url": "",
        #   "auth_provider_x509_cert_url": "https: //www.googleapis.com/oauth2/v1/certs"}}

    else:
        # With secrets baked here for my native app.
        CLIENT_ID = '.....'
        CLIENT_SECRET = '.....'

        # Note: You could also have used 'http://localhost' to redirect.
        flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                                   client_secret=CLIENT_SECRET,
                                   scope=scope,
                                   redirect_uri='urn:ietf:wg:oauth:2.0:oob')

    http = httplib2.Http()
    http.disable_ssl_certificate_validation = True

    storage = Storage(storage_filename)
    credentials = storage.get()
    if credentials is None:
        credentials = tools.run_flow(flow, storage, opts, http=http)

    credentials.authorize(http)

    return http


def main():
    parser = argparse.ArgumentParser(description=__doc__.strip(),
                                     parents=[tools.argparser])
    parser.add_argument('--storage', action='store',
                        default=path.join(os.environ['HOME'], '.oauth2-for-google-apis'),
                        help="Storage filename")
    opts = parser.parse_args()

    # Connect, with authentication.
    # Check https://developers.google.com/drive/scopes for all available scopes.
    DRIVE_SCOPE = 'https://www.googleapis.com/auth/drive'
    http = get_authenticated_http(DRIVE_SCOPE, opts.storage, opts)

    # Access the drive API.
    drive = googleapiclient.discovery.build('drive', 'v2', http=http)

    experiment(drive)


def experiment(drive):
    """Toy around and experiment with the Google Drive API.

    Args:
      drive: A googleapiclient Drive stub.
    """

    # about() API.
    if 0:
        about = drive.about().get().execute()
        pp(about['name'])

    # files() and children() API.
    if 0:
        filelist = drive.files().list(q="'0Bxq3M95KLnV5VHdUQnRVUVRJM1k' in parents", maxResults=1000).execute()
        #pp(filelist)
        # filelist = drive.children().list(folderId='0Bxq3M95KLnV5VHdUQnRVUVRJM1k', maxResults=1000).execute()
        assert 'nextPageToken' not in filelist
        for item in filelist['items']:
            print "{:48} {:64} {}".format(*map(item.get, 'id mimeType title'.split()))
            if 0:
                print
                pp(item.get('webContentLink'))
                pp(item.get('alternateLink'))
                pp(item.get('downloadUrl'))


    # Download a file's contents in various formats.
    index_id = '1RaondTJCS_IUPBHFNdT8oqFKJjVJDsfsn6JEjBG04eA'
    returns_id = '1vEFB44-HFqydYVJXA-QxT4AN0K5xHHfSkhTmRSCPkac'
    id_ = index_id

    index_metadata = drive.files().get(fileId=id_).execute()
    pp(index_metadata)
    for mime_type in ['application/pdf',
                      'text/html',
                      'text/plain',
                      'application/rtf',
                      'application/vnd.oasis.opendocument.text']:
        url = index_metadata['exportLinks'][mime_type]
        filename = '/tmp/index.{}'.format(mime_type.replace('/', '.'))
        filename, unused_headers = urllib.urlretrieve(url, filename)
        print filename


if __name__ == '__main__':
    main()
