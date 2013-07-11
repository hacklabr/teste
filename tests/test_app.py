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
        MyModel,
    )
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        model = MyModel(name='one', value=55)
        DBSession.add(model)


def teardown():
    DBSession.remove()
    testing.tearDown()


def test_it():
    from timtec.views import my_view
    request = testing.DummyRequest()
    info = my_view(request)
    assert info['one'].name == 'one'
    assert info['project'] == 'timtec'
