import os,datetime,time

from flask import request, redirect, url_for, render_template, Response
from flask_login import login_manager, login_user, LoginManager, current_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

from database import user as User
from database import userrelationship

from . import users
from database import DBSession

from app import mail,Message

@users.route('/login', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        next = request.form['nexturl']
        print(next)
        if next == 'None': next = url_for('main')
        email = request.form['email']
        password = request.form['password']
        connect = DBSession()
        try:
            user = connect.query(User).filter(User.email == email).first()
            print(user.get_id())
            if email != '' and check_password_hash(user.password, password):
                login_user(user)
                connect.close()
                return redirect(next or url_for('main'))
                # return render_template('main.html', user=user.username,current_time=current_time)
            else:
                connect.close()
                return render_template('login.html', msg='登录失败，请检查邮箱和密码！')
        except:
            connect.close()
            return render_template('login.html', msg='用户名{0}无效!'.format(email))
    else:
        next = request.values.get('next')
        print(next)
        return render_template('login.html', nexturl=next)


@login_required
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.userlogin'))


def gen_token(userid, expiration=3600):  # 单位为秒, 设定31天过期
    s = Serializer('`~1!2@3#4$5%6^7&8*9(0)-_=+', expires_in=expiration)
    return s.dumps({'id': userid})  # user为model中封装过的对象


@users.route('/register', methods=['GET', 'POST'])
def userregister():
    if request.method == 'POST':
        session = DBSession()
        email = request.form['useremail']
        username = request.form['username']
        password = request.form['userpassword']
        password = generate_password_hash(password)
        print(email)
        if session.query(User).filter(User.email == email).first():
            return render_template('register.html', msg='该邮箱已被注册！')
        else:
            adduser = User(password=password, username=username, email=email, admin=0,activated=0)
            session.add(adduser)
            session.commit()
            os.makedirs(os.path.join(os.getcwd(),'static','files','{0}'.format(adduser.userid)))
            url='http://47.94.138.25/activate/{0}'.format(gen_token(adduser.userid))
            # message=Message('Account authorize',sender='13517078184@163.com',recipients=['{}'.format(username),'{}'.format(email)])
            message = Message('Account authorize', sender='13517078184@163.com',recipients=['13517078184@139.com'])
            message.body="Hello,{0}<br>This email is from admin!<br>Your account has not been activated yet!<br><a href='{1}'>click here to activate your account!</a><br>if you mistaken the email,please ignore it!".format(username,url)
            mail.send(message)
            session.close()

            return redirect(url_for('users.userlogin'))
    else:
        return render_template('register.html')


@login_required
@users.route('/addfriend/<email>', methods=['GET', 'POST'])
def useraddfriend(email):
    if request.method == 'GET':
        session = DBSession()
        user = current_user._get_current_object()
        friend=session.query(User).filter(User.email == email).first()
        userid=friend.userid
        if session.query(userrelationship).filter(userrelationship.user == user.userid,
                                                  userrelationship.friend == userid).first():
            #  user has been send request
            return Response(response='You have been send request or already friend!', status=400)
        if userid == user.userid:
            return Response(response='Failed!', status=400)
        else:
            # now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            userre = userrelationship(user=user.userid, friend=userid, flag=0,rtime=now)
            session.add(userre)
            session.commit()
            session.close()
            return Response(response='successfully!', status=200)


@login_required
@users.route('/accfriend/<userid>', methods=['GET', 'POST'])
def useraccfriend(userid):
    if request.method == 'GET':
        session = DBSession()
        user = current_user._get_current_object()
        if userid == user.userid:
            return Response(response='Failed!', status=400)
        else:
            now=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            userre = userrelationship(user=user.userid, friend=userid, flag=1,rtime=now)
            session.add(userre)
            fr=session.query(userrelationship).filter(userrelationship.user == userid,
                                                  userrelationship.friend == user.userid).first()
            fr.flag=1
            fr.rtime=now
            session.commit()
            session.close()
            return Response(response='successfully!', status=200)

@login_required
@users.route('/delfriend/<userid>', methods=['GET', 'POST'])
def useradelfriend(userid):
    if request.method == 'GET':
        session = DBSession()
        user = current_user._get_current_object()
        if userid == user.userid:
            return Response(response='Failed!', status=400)
        else:
            userfriend=session.query(userrelationship).filter(userrelationship.user == userid,userrelationship.friend == user.userid).first()
            friend=session.query(userrelationship).filter(userrelationship.user == user.userid,userrelationship.friend == userid).first()
            session.delete(userfriend)
            session.delete(friend)
            session.commit()
            session.close()
            return Response(response='successfully!', status=200)



@users.route('/activate/<token>',methods=['GET','POST'])
def activate_account(token):
    if request.method=='GET':
        session=DBSession()
        s = Serializer('`~1!2@3#4$5%6^7&8*9(0)-_=+')
        try:
            data=s.loads(token)
            print(data['id'])
            if session.query(User).filter(User.userid==data['id']).first():
                user = session.query(User).filter(User.userid == data['id']).first()
                user.activated=1
                return 'user:{0} has been activated!'.format(user.username)
            else: return 'userid:{0} is invalid!'.format(data['id'])


        except SignatureExpired or BadSignature:
            return 'token is invalid!'
