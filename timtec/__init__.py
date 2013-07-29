from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from hem.interfaces import IDBSession
from pyramid_beaker import session_factory_from_settings
from .models import (
    DBSession,
    Base,
)
from . import models


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings)
    config.set_session_factory(session_factory)
    config.registry.registerUtility(DBSession, IDBSession)
    # config.scan_horus(models)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan_horus(models)
    config.add_route('index', '/')
    config.add_route('course_intro', '/{course}/intro')
    config.add_route('lesson', '/{course}/{lesson}/')
    config.include('horus')
    config.include('pyramid_mailer')
    # formalchemy
    config.include('pyramid_formalchemy')
    config.include('pyramid_fanstatic')
    config.include('fa.jquery')
    # register an admin UI
    config.formalchemy_admin('/admin', package='timtec', view='fa.jquery.pyramid.ModelView')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()
