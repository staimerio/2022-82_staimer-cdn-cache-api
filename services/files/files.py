# Retic
from retic import env, App as app

# Services
from retic.services.responses import success_response_service, error_response_service
from retic.services.general.json import jsonify, parse

# Requests
import requests

import base64

# contants
URL_SENDFILES_FILES_FOLDER = app.apps['backend']['sendfiles']['base_url'] + \
    app.apps['backend']['sendfiles']['files_folder']
URL_SENDFILES_DOWNLOADS_FILES = app.apps['backend']['sendfiles']['base_url'] + \
    app.apps['backend']['sendfiles']['downloads_files']
CACHE_FOLDER_PATH = app.config.get('CACHE_FOLDER_PATH')
CACHE_BASE_PATH = app.config.get('CACHE_BASE_PATH')


def get_from_source(source, file, web=None):
    """Get a file from a url

    :param source: URL that will be use to get the file
    """

    try:
        """Prepare the payload"""
        _url = source

        """Fetch file from the URL"""
        _file_req = requests.get(
            _url
        )

        """Check if the response is valid"""
        if _file_req.status_code != 200:
            """Return error if the response is invalid"""
            return _file_req.json()

        _filepath_web = "{0}/{1}".format("https://{0}/images-cache".format(web)
                                        if web else CACHE_BASE_PATH, file)

        """Define the response object"""
        _response = {
            u'body': _file_req.content,
            u'url': _filepath_web
        }

        """Return data"""
        return success_response_service(data=_response)
    except Exception as error:
        return error_response_service(msg=str(error))


def get_from_source_encoded(source, file, web):
    """Get a file from a url

    :param source: URL that will be use to get the file
    """
    return get_from_source(base64.b64decode(source), file, web)
