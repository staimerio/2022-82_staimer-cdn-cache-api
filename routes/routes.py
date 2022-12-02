# Retic
from retic import Router
from retic.lib.hooks.middlewares import cors

# Controllers
import controllers.cache as cache

"""Define Router instance"""
router = Router()

"""Define CORS"""
_cors = cors(
    headers="Content-Type,source",
    expose_headers="Content-Type,source"
)

"""Add cors settigns"""
router.use(_cors)

"""Define the options methods for all routes"""
router.options("/*", _cors)

router \
    .get("/images/:file", cache.get_by_id_param)