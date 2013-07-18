import transaction

from pyramid import testing

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
