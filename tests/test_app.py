import transaction
from pkg_resources import resource_filename
from pyramid import (
    testing,
    router,
)
from timtec.models import DBSession

config = None


def setup():
    global config
    config = testing.setUp()
    from sqlalchemy import create_engine
    engine = create_engine('sqlite://')
    from timtec.models import (
        Base,
        User
    )
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        model = User(username='one', password='kdkdk', email='skdsk', id='kkk', pk='kk')
        DBSession.add(model)


def teardown():
    DBSession.remove()
    testing.tearDown()


def test_it():
    from timtec.views import my_view
    request = testing.DummyRequest()
    info = my_view(request)
    assert info['one'].username == 'one'
    assert info['project'] == 'timtec'

def test_app_creation():
    from paste.deploy.loadwsgi import appconfig
    from timtec import main
    settings = appconfig('config:' + resource_filename(__name__, '../development.ini'))
    app = main(config, **settings)
    assert isinstance(app, router.Router)
