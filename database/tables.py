from flask_sqlalchemy import Model
from sqlalchemy import *
from sqlalchemy import String, INTEGER, ForeignKey, Column, TEXT, SmallInteger, TIMESTAMP
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

Base = declarative_base()


class user(UserMixin, Base, Model):
    __tablename__ = 'user'
    userid = Column(INTEGER, primary_key=True, autoincrement=True, )
    username = Column(String(45))
    admin = Column(SmallInteger)  # 1 is admin
    email = Column(String(100))
    password = Column(String(93))
    activated=Column(SmallInteger)
    def get_id(self):
        return self.userid

    def isAdmin(self):
        return self.admin

    def __repr__(self):
        return "<user(userid={0},username={1},email={2},level={3})>".format(self.userid, self.username, self.email,
                                                                            self.admin)


class userrelationship(Base):
    __tablename__ = 'relationship'
    user = Column(Integer, ForeignKey('user.userid'),primary_key=True)
    friend = Column(Integer, ForeignKey('user.userid'),primary_key=True)
    flag = Column(SmallInteger)
    rtime=Column(TIMESTAMP)
    # user = relationship('user', backref('userrelationship', order_by=user))

    def __repr__(self):
        return "<relationship(user={0},friend={1},flag={2},rtime={3})>".format(self.user, self.friend,
                                                                        self.flag,self.rtime)

class files(Base):
    __tablename__ = 'files'
    fileid = Column(INTEGER, primary_key=True, autoincrement=True)
    filename = Column(String(100))
    filepath = Column(String(150))
    uploadtime = Column(TIMESTAMP)
    user_userid = Column(Integer, ForeignKey('user.userid'))
    quote=Column(INTEGER)

    # user = relationship('user', backref=backref('files', order_by=user_userid))

    def get_id(self):
        return self.fileid

    def __repr__(self):
        return "<files(fileid={0},filename={1},filepath={2},uploadtime={3},user_userid={4},quote={5})>".format(
            self.fileid, self.filename, self.filepath, self.uploadtime, self.user_userid,self.quote
        )


class filerecord(Base):
    __tablename__ = 'filerecord'
    user_userid = Column(Integer, ForeignKey('user.userid'),primary_key=True)
    files_fileid = Column(Integer, ForeignKey('files.fileid'),primary_key=True)
    flag=Column(SmallInteger)
    recordtime=Column(TIMESTAMP)

    # user = relationship('user', backref=backref('files', order_by=user_userid))
    # files = relationship('files', backref=backref('files', order_by=files_fileid))

    def __repr__(self):
        return "<filerecord(user_userid={0},files_fileid={1},deltime={2}),flag={3}>".format(self.user_userid,self.files_fileid,self.recordtime,self.flag)


class sendrecord(Base):
    __tablename__ = 'sendrecord'
    user_userid = Column(Integer, ForeignKey('user.userid'),primary_key=True)
    user_userid1 = Column(Integer, ForeignKey('user.userid'),primary_key=True)
    files_fileid = Column(Integer, ForeignKey('files.fileid'),primary_key=True)
    sendtime = Column(TIMESTAMP)
    note = Column(TEXT)

    # user = relationship('user', backref=backref('files', order_by=user_userid))
    # files = relationship('files', backref=backref('files', order_by=files_fileid))

    def __repr__(self):
        return "<sendrecord(user_userid={0},user_userid={1},files_fileid={2},sendtime={3},note={4})>".format(self.user_userid,self.user_userid1,self.files_fileid,self.sendtime,self.note)