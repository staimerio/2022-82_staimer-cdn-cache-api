"""Services for the Cache controller"""

# Logging
import logging

# Retic
from retic import env, App as app

# Services
from retic.services.responses import success_response_service, error_response_service
from retic.services.general.json import parse, jsonify

# Utils
from services.general.general import get_content_from_file, save_content_in_file
from services.general.general import isfile, rmtree, mkdir, isdir

# Constants
CACHE_FOLDER_PATH = app.config.get('CACHE_FOLDER_PATH')
CACHE_BASE_PATH = app.config.get('CACHE_BASE_PATH')


def save_file_cache(file, body, extension=''):
    """Save a file in cache storage

    :param filepath: Path of the file to write information.
    :param bfile: File to save
    """
    """Prepara all parameters"""
    _filepath = "{0}/{1}{2}".format(CACHE_FOLDER_PATH, file, extension)

    """Check if the file exists"""
    _exists = isdir(CACHE_FOLDER_PATH)

    """If it is'nt exists, return a error"""
    # logging.warning('*****************************************')
    # logging.warning('_exists')
    # logging.warning(_exists)
    if _exists:
        """Save file"""
        save_content_in_file(_filepath, body, mode='wb')


def clean_cache_files():
    """Delete the files cache folder"""
    try:
        """Check if the file exists"""
        _exists = isdir(CACHE_FOLDER_PATH)

        """If it is'nt exists, return a error"""
        if not _exists:
            raise Exception("Bad request.")

        """Delete the cache folder for files"""
        rmtree(CACHE_FOLDER_PATH)

        """Create the cache folder for files"""
        mkdir(CACHE_FOLDER_PATH)

        """Response to request"""
        return success_response_service(
            msg="Files deleted."
        )
    except Exception as err:
        return error_response_service(
            msg=str(err)
        )


def exists_by_id_cache(file):
    """Find a file on cache storage

    :param file: Id of the file, it's the name in the cache storage
    """
    try:
        """Prepara all parameters"""
        _filepath = "{0}/{1}".format(CACHE_FOLDER_PATH, file)

        """Check if the file exists"""
        _exists = isfile(_filepath)

        if not _exists:
            return error_response_service(msg='Not found.')
        _filepath_web = "{0}/{1}".format(CACHE_BASE_PATH, file)
        return success_response_service(data={u"url": _filepath_web})
    except Exception as error:
        return error_response_service(msg=str(error))
