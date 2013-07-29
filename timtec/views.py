from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.orm import joinedload
from .models import (
    DBSession,
    Course,
    Lesson,
)


class BaseView(object):
    def __init__(self, request):
        self.request = request


class CourseController(BaseView):
    @view_config(route_name='index', renderer='templates/course_intro.pt')
    @view_config(route_name='course_intro', renderer='templates/course_intro.pt')
    def intro(self):
        course_slug = self.request.matchdict.get('course', 'dbsql')
        course = DBSession.query(Course).filter(Course.slug == course_slug).first()
        return {u'course': course}

    @view_config(route_name='lesson', renderer='templates/lesson.pt')
    def lesson(self, course_slug=u'dbsql'):
        course_slug = self.request.matchdict['course']
        lesson_name = self.request.matchdict['lesson']
        lesson = DBSession.query(Lesson).join(Course).filter(Lesson.name == lesson_name).filter(Course.slug == course_slug).first()
        return {u'lesson': lesson}
