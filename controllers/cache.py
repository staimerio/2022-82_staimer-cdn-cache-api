
# Logging
import logging
# Retic
from retic import Request, Response, Next

# Services
from retic.services.validations import validate_obligate_fields
from retic.services.responses import error_response_service, success_response_service
from services.cache import cache
from services.files import files, photos


def get_by_id_param(req: Request, res: Response):
    """Get a file from his Id"""

    """Find file in the cache storage"""
    _file_cache = cache.exists_by_id_cache(req.param('file'), req.host)

    """If it's exists, response to client"""
    if _file_cache['valid']:
        return res.redirect(_file_cache['data']['url'])

    """Check that all params are valid"""
    _validate = validate_obligate_fields({
        u'id': req.param('id'),
    })

    """Si existen problemas, retornar un mensaje de error"""
    if _validate["valid"] is False:
        return res.bad_request(
            error_response_service(
                "The header {} is necesary.".format(_validate["error"])
            )
        )

    """If it's not exists, get from the source main server"""
    _file_req = files.get_from_source_encoded(
        req.param('id'),
        req.param('file'),
        req.host
    )
    """Check if the file exists"""
    if not _file_req['valid']:
        return res.bad_request(_file_req)

    """Save file in the cache storage"""
    _url=cache.save_file_cache(
        req.param('file'),
        _file_req['data']['body']
    )

    return res.redirect(_file_req['data']['url'])
