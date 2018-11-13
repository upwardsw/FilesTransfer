import os, time, datetime

from flask import render_template, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import files as fbp

from database import files, filerecord, DBSession, sendrecord, userrelationship
from database import user as User


@fbp.route('/upload', methods=['GET', 'POST'])
@login_required
def filesupload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            session = DBSession()
            filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S_")+secure_filename(file.filename)
            user = current_user._get_current_object()
            filepath = os.path.join(os.getcwd(), 'static', 'files', '{}'.format(user.userid))
            # now=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(time.time())))
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(now)
            print(filepath)
            # file.save(os.path.join(os.getcwd(),'static',filename))
            file.save(os.path.join(filepath, filename))
            filerec = files(filename=filename, filepath=filepath, user_userid=user.userid, uploadtime=now, quote=1)
            session.add(filerec)
            session.commit()
            record = filerecord(user_userid=user.userid, files_fileid=filerec.fileid, flag=1, recordtime=now)
            session.add(record)
            session.commit()
            session.close()
            return 'File {0} has benn saved in {1} !'.format(filename, filepath)
    else:
        return render_template('uploadtest.html')


@fbp.route('/delfile/<fileid>')
@login_required
def filesdelfile(fileid):
    if request.method == 'GET':
        session = DBSession()
        user = current_user._get_current_object()
        # print(session.query(filerecord).filter(filerecord.files_fileid == fileid).count())
        try:
            record = session.query(filerecord).filter(filerecord.files_fileid == fileid,
                                                      filerecord.user_userid == user.userid).first()
            record.flag = 0
            session.commit()
            delfile = session.query(files).filter(files.fileid == fileid).first()
            delfile.quote -= 1
            session.commit()
            session.close()
            # if session.query(filerecord).filter(filerecord.files_fileid==fileid).count()==0:
            #     changefile=session.query(files).filter(files.fileid==fileid).first()
            #     # now=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(time.time())))
            #     now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #     changefile.filedestime=now
            #     session.commit()
            return 'delete file successfully!'
        except:
            return 'no such file'


@fbp.route('/delhistory/<fileid>')
@login_required
def delhistoryfile(fileid):
    if request.method == 'GET':
        session = DBSession()
        user = current_user._get_current_object()
        # print(session.query(filerecord).filter(filerecord.files_fileid == fileid).count())
        try:
            record = session.query(filerecord).filter(filerecord.files_fileid == fileid,
                                                      filerecord.user_userid == user.userid).first()
            if record.flag == 0:
                session.delete(record)
                session.commit()
                session.close()
                # if session.query(filerecord).filter(filerecord.files_fileid==fileid).count()==0:
                #     changefile=session.query(files).filter(files.fileid==fileid).first()
                #     # now=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(time.time())))
                #     now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                #     changefile.filedestime=now
                #     session.commit()
                return 'delete record successfully!'
            else:
                return 'warning:record is valid!'
        except:
            return 'no such record'


@fbp.route('/recoveryfile/<fileid>')
@login_required
def recoveryfile(fileid):
    if request.method == 'GET':
        session = DBSession()
        user = current_user._get_current_object()
        # print(session.query(filerecord).filter(filerecord.files_fileid == fileid).count())
        try:
            record = session.query(filerecord).filter(filerecord.files_fileid == fileid,
                                                      filerecord.user_userid == user.userid).first()
            record.flag = 1
            session.commit()
            delfile = session.query(files).filter(files.fileid == fileid).first()
            delfile.quote += 1
            session.commit()
            session.close()
            # if session.query(filerecord).filter(filerecord.files_fileid==fileid).count()==0:
            #     changefile=session.query(files).filter(files.fileid==fileid).first()
            #     # now=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(time.time())))
            #     now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #     changefile.filedestime=now
            #     session.commit()
            return 'recovery record successfully!'
        except:
            return 'no such record'


@fbp.route('/sendfile/<recuserid>/<fileid>/<note>', methods=['GET', 'POST'])
@login_required
def sendfile(recuserid, fileid, note):
    session = DBSession()
    senduser = current_user._get_current_object()
    print(senduser)
    print(recuserid, fileid, note)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if note is None or note == 'None': note = '00'
    if session.query(User).filter(User.userid == recuserid).first() and session.query(filerecord).filter(
            filerecord.files_fileid == fileid, filerecord.flag == 1,
            filerecord.user_userid == senduser.userid).first() and recuserid != senduser.userid and (
            session.query(userrelationship).filter(userrelationship.user == recuserid,
                                                   userrelationship.friend == senduser.userid).first() and session.query(
        userrelationship).filter(userrelationship.user == senduser.userid,
                                 userrelationship.friend == recuserid).first()):
        src = sendrecord(user_userid=senduser.userid, user_userid1=recuserid, files_fileid=fileid, sendtime=now,
                         note=note)
        session.add(src)
        session.commit()
        recfile = filerecord(user_userid=recuserid, files_fileid=fileid, flag=1, recordtime=now)
        session.add(recfile)
        session.commit()
        filequote = session.query(files).filter(files.fileid == fileid).first()
        filequote.quote += 1
        filename = filequote.filename
        session.commit()
        session.close()
        return 'send file:{0} successfully!'.format(filename)
    else:
        return 'send fail!'
