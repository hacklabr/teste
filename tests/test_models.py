from pyramid import testing
from paste.deploy.loadwsgi import appconfig

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from timtec.models import (
    DBSession,
    Base,
)
import os
here = os.path.dirname(__file__)
settings = appconfig('config:' + os.path.join(here, '../', 'test.ini'))


# def setup_module(module):
#     engine = engine_from_config(settings, prefix='sqlalchemy.')
#     DBSession.configure(bind=engine)
#     Base.metadata.create_all(engine)


class BaseModelTest():
    @classmethod
    def setup_class(cls):
        cls.engine = engine_from_config(settings, prefix='sqlalchemy.')
        cls.Session = sessionmaker()
        Base.metadata.create_all(cls.engine)

    def setup_method(self, method):
        connection = self.engine.connect()

        # begin a non-ORM transaction
        self.trans = connection.begin()

        # bind an individual Session to the connection
        DBSession.configure(bind=connection)
        self.session = self.Session(bind=connection)
        Base.session = self.session
#         Base.metadata.create_all(connection)

    def teardown_method(self, method):
        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        testing.tearDown()
        self.trans.rollback()
        self.session.close()


class TestVideo(BaseModelTest):
    def test(self):
        from timtec.models import Video
        video = Video(name='Video de teste', url='http://timtec.com.br')
        self.session.add(video)
        self.session.commit()
        query = self.session.query(Video.name).filter_by(name='Video de teste')
        name = query.all()[0][0]
        assert video.name == name
