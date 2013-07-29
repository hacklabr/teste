from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.orm import joinedload
from .models import (
    DBSession,
    Course,
)


class BaseView(object):
    def __init__(self, request):
        self.request = request


class CourseController(BaseView):
    @view_config(route_name='index', renderer='templates/course_intro.pt')
    @view_config(route_name='course_intro', renderer='templates/course_intro.pt')
    def intro(self, course_slug=u'dbsql'):
        course = DBSession.query(Course).options(joinedload(Course.professors)).filter(Course.slug == course_slug).first()
        return {
            u'name': u'timtec',
            u'course': course}

# @view_config(route_name='index', renderer='templates/course_intro.pt')
# @view_config(route_name='course_intro', renderer='templates/course_intro.pt')
# def course_intro(request):
    # DBSession.query(Course).filter(Course.name == 'one').first()


@view_config(route_name='klass', renderer='templates/klass.pt')
def klass(request):
    return {}
