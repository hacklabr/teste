# coding: utf-8

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


class BaseTestCase():
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


class TestVideo(BaseTestCase):
    def test(self):
        from timtec.models import Video
        video = Video(name='Video de teste', youtube_id='http://timtec.com.br')
        self.session.add(video)
        self.session.commit()
        query = self.session.query(Video.name).filter_by(name='Video de teste')
        name = query.all()[0][0]
        assert video.name == name


class TestViews(BaseTestCase):

#     def setup_method(self, method):
#         self.config = testing.setUp(request=testing.DummyRequest())
#         super(TestViews, self).setup_method()

    def test_course_intro(self):
        from timtec.views import CourseController
        from timtec.models import (
           Course,
           CourseProfessors,
           User,
        )
        course = Course()
        course.slug = u'dbsql'
        course.name = u'Banco de Dados e SQL'
        course.description = u'Introdução a Bancos de Dados e Linguagem SQL'

        user = User(username='ramalho', password='kdkdk', email='skdsk@vcx')
        user.name = u'Luciano Ramalho'
        course_professors = CourseProfessors()
        course_professors.user = user
        course_professors.biography = (
            u'Mussum ipsum cacilds, vidis litro abertis. Consetis'
            u'adipiscings elitis. Pra lá , depois divoltis porris,'
            u'paradis. Paisis, filhis, espiritis santis. Mé faiz elementum'
            u' girarzis, nisi eros vermeio, in elementis mé pra quem é'
            u'amistosis quis leo. Manduma pindureta quium dia nois paga.'
            u'bolis eu num gostis.'
        )
        course.professors.append(course_professors)
        DBSession.add(course)

        request = testing.DummyRequest()
        request.matchdict['course'] = u'dbsql'
        course_controller = CourseController(request)
        response = course_controller.intro()
        assert response['course'] == course
        assert response['course'].professors[0] == course_professors
        assert response['course'].professors[0].user == user
