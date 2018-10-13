from flask_sqlalchemy import Model
from sqlalchemy import *
from sqlalchemy import String, INTEGER, ForeignKey, Column, TEXT, SmallInteger, TIMESTAMP
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

Base = declarative_base()


class user(UserMixin, Base, Model):
    __tablename__ = 'user'
    userid = Column(INTEGER, primary_key=true, autoincrement=True, )
    username = Column(String(45))
    level = Column(SmallInteger)  # 0 is admin
    email = Column(String(100))
    password = Column(93)

    def get_id(self):
        return self.userid

    def notAdmin(self):
        return self.level

    def __repr__(self):
        return "<user(userid={0},username={1},email={2},level={3})>".format(self.userid, self.username, self.email,
                                                                            self.level)


class userrelationship(Base):
    __tablename__ = 'relationship'
    user = Column(Integer, ForeignKey('user.userid'))
    friend = Column(Integer, ForeignKey('user.userid'))
    flag = Column(SmallInteger)

    user = relationship('user', backref('userrelationship', order_by=user))

    def __repr__(self):
        return "<relationship(user={0},friend={1},flag={2})>".format(self.user, self.friend,
                                                                        self.flag)

class files(Base):
    __tablename__ = 'files'
    fileid = Column(INTEGER, primary_key=True, autoincrement=True)
    filename = Column(String(100))
    filepath = Column(String(150))
    uploadtime = Column(TIMESTAMP)
    user_userid = Column(Integer, ForeignKey('user.userid'))
    filedestime = Column(TIMESTAMP)

    user = relationship('user', backref=backref('files', order_by=user_userid))

    def get_id(self):
        return self.fileid

    def __repr__(self):
        return "<files(fileid={0},filename={1},filepath={2},uploadtime={3},user_userid={4})>".format(
            self.fileid, self.filename, self.filepath, self.uploadtime, self.user_userid
        )


class filerecord(Base):
    __tablename__ = 'filerecord'
    user_userid = Column(Integer, ForeignKey('user.userid'))
    files_fileid = Column(Integer, ForeignKey('files.fileid'))
    deltime = Column(TIMESTAMP)

    user = relationship('user', backref=backref('files', order_by=user_userid))
    files = relationship('files', backref=backref('files', order_by=files_fileid))

    def __repr__(self):
        return "<filerecord(user_userid={0},files_fileid={1},deltime={2})>".format(self.user_userid,self.files_fileid,self.deltime)


class sendrecord(Base):
    __tablename__ = 'sendrecord'
    user_userid = Column(Integer, ForeignKey('user.userid'))
    user_userid1 = Column(Integer, ForeignKey('user.userid'))
    files_fileid = Column(Integer, ForeignKey('files.fileid'))
    sendtime = Column(TIMESTAMP)
    note = Column(TEXT)

    user = relationship('user', backref=backref('files', order_by=user_userid))
    files = relationship('files', backref=backref('files', order_by=files_fileid))

    def __repr__(self):
        return "<sendrecord(user_userid={0},user_userid={1},files_fileid={2},sendtime={3},note={4})>".format(self.user_userid,self.user_userid1,self.files_fileid,self.sendtime,self.note)