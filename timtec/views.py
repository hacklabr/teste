from pyramid.response import Response
from pyramid.view import view_config

from .models import (
    DBSession,
    Course,
)


@view_config(route_name='index')
@view_config(route_name='course_intro', renderer='templates/course_intro.pt')
def course_intro(request):

    # DBSession.query(Course).filter(Course.name == 'one').first()
    return {'name': 'timtec'}

@view_config(route_name='klass', renderer='templates/klass.pt')
def klass(request):
    return {}
