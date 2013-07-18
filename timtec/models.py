import re
import sqlalchemy as sa
from sqlalchemy.ext.declarative import (
    declarative_base,
    declared_attr,
)
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from zope.sqlalchemy import ZopeTransactionExtension
from horus.models import (
    GroupMixin,
    UserMixin,
    UserGroupMixin,
    ActivationMixin,
)


class BaseModel(object):
    """Base class which auto-generates tablename, and surrogate
    primary key column.
    """
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    @declared_attr
    def pk(self):
        # We use pk instead of id because id is a python builtin
        return sa.Column(sa.Integer, primary_key=True)

    _traversal_lookup_key = 'pk'

    @declared_attr
    def __tablename__(cls):
        """Convert CamelCase class name to underscores_between_words
        table name."""
        name = cls.__name__.replace('Mixin', '')

        return (
            name[0].lower() +
            re.sub(r'([A-Z])', lambda m: "_" + m.group(0).lower(), name[1:])
        )


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base(cls=BaseModel)


class User(UserMixin, Base):
    pass


class Group(GroupMixin, Base):
    pass


class UserGroup(UserGroupMixin, Base):
    pass


class Activation(ActivationMixin, Base):
    pass


class Video(Base):
    name = sa.Column(sa.Unicode(255), nullable=False)


class Course(Base):
    """Course """
    name = sa.Column(sa.Unicode(255), nullable=False)
    description = sa.Column(sa.Text(255))
    knowledge_acquired = sa.Column(sa.Text(255))
    knowledge_required = sa.Column(sa.Text(255))
    professors = sa.Column(sa.Integer, sa.ForeignKey("{0}.pk".format(User.__tablename__)))
    intro_video = sa.Column(sa.Integer, sa.ForeignKey("{0}.pk".format(Video.__tablename__)))
    students = sa.Column(sa.Integer, sa.ForeignKey("{0}.pk".format(User.__tablename__)))
#     wiki
#     forum
#     notes


class CourseClass(Base):
    name = sa.Column(sa.Unicode(255), nullable=False)
