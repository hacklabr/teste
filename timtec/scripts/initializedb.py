# coding: utf-8

import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from ..models import (
    DBSession,
    Base,
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def initial_dev_data():
    from ..models import (
        User,
        Course,
        Lesson,
        CourseProfessors,
    )
    with transaction.manager:
        course = Course()
        course.slug = u'dbsql'
        course.name = u'Banco de Dados e SQL'
        course.description = u'Introdução a Bancos de Dados e Linguagem SQL'
        course.abstract = (
            u'Mussum ipsum cacilds, vidis litro abertis. Consetis'
            u'adipiscings elitis. Pra lá , depois divoltis porris,'
            u'paradis. Paisis, filhis, espiritis santis. Mé faiz elementum'
            u' girarzis, nisi eros vermeio, in elementis mé pra quem é'
            u'amistosis quis leo. Manduma pindureta quium dia nois paga.'
            u' Sapien in monti palavris qui num significa nadis i pareci '
            u'latim. Interessantiss quisso pudia ce receita de bolis, mais '
            u'bolis eu num gostis.'
        )

        course.knowledge_acquired = (
            u'Suco de cevadiss, é um leite divinis, qui tem lupuliz, matis, aguis'
            u' e fermentis. Interagi no mé, cursus quis, vehicula ac nisi. Aenean '
            u'vel dui dui. Nullam leo erat, aliquet quis tempus a, posuere ut mi. '
            u'Ut scelerisque neque et turpis posuere pulvinar pellentesque nibh ullamcorper. '
            u'Pharetra in mattis molestie, volutpat elementum justo. Aenean ut ante turpis. '
            u'Pellentesque laoreet mé vel lectus scelerisque interdum cursus velit auctor. '
            u'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam ac mauris lectus, '
            u'non scelerisque augue. Aenean justo massa.'

        )
        course.knowledge_required = (
            u'Casamentiss faiz malandris se pirulitá, Nam liber tempor cum soluta nobis eleifend '
            u'option congue nihil imperdiet doming id quod mazim placerat facer possim assum. '
            u'Lorem ipsum dolor sit amet, consectetuer Ispecialista im mé intende tudis nuam golada, '
            u'vinho, uiski, carirí, rum da jamaikis, só num pode ser mijis. Adipiscing elit, sed '
            u'diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. '
            u'Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis '
            u'nisl ut aliquip ex ea commodo consequat.'
        )
        course.time_estimated = u'1 mês'
        course.extra_dadication = u'40 horas'

        lessons = [
           (u'Apresentando: Bancos de Dados', u'Para que servem os bancos de dados'),
           (u'Programas para operar bancos de dados', u'Software para bancos de dados'),
           (u'O que é SQL', u'Ésse-quê-éle'),
           (u'Organizando os dados', u'Organizando os dados'),
           (u'Instalar e testar o SQLite', u'Instalar os programas para praticar'),
        ]

        for lesson_title, lesson_desc in lessons:
            lesson = Lesson()
            lesson.name = lesson_title
            lesson.desc = lesson_desc
            course.lessons.append(lesson)
            DBSession.add(lesson)

        user1 = User(username='ramalho', password='kdkdk', email='skdsk@vcx')
        user1.name = u'Luciano Ramalho'
        professor2 = User(username='Lucia', password='kdkdk', email='skdsk@asdf')
        professor2.name = u'Lucia Silva'
        DBSession.add(user1)
        DBSession.add(professor2)

        course_professor = CourseProfessors()
        course_professor.user = user1
        course_professor.biography = (
            u'Mussum ipsum cacilds, vidis litro abertis. Consetis'
            u'adipiscings elitis. Pra lá , depois divoltis porris,'
            u'paradis. Paisis, filhis, espiritis santis. Mé faiz elementum'
            u' girarzis, nisi eros vermeio, in elementis mé pra quem é'
            u'amistosis quis leo. Manduma pindureta quium dia nois paga.'
            u'bolis eu num gostis.'
        )
        DBSession.add(course_professor)
        course.professors.append(course_professor)

        course_professors2 = CourseProfessors()
        course_professors2.user = professor2
        course.professors.append(course_professors2)
        DBSession.add(course_professors2)

        DBSession.add(course)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    initial_dev_data()
