import os

from flask import Flask, send_from_directory
from flask import request, render_template
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_login import LoginManager
from flask_login import login_required
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message

from database import DBSession
from database import user as User
from files import files as files_blueprint
from users import users as user_blueprint

app = Flask(__name__)
mail=Mail()

app.config['SECRET_KEY'] = '`~1!2@3#4$5%6^7&8*9(0)-_=+'
app.config['MAIL_SERVER'] = '220.181.12.16'
# app.config['MAIL_SERVER'] = 'smtp.163.com'  #  这里用163邮件服务器
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True        # 启用安全传输层协议
app.config['MAIL_USERNAME'] = '13517078184@163.com'      # 从系统环境变量加载用户名和密码
app.config['MAIL_PASSWORD'] = '5609651wmm'

# msg = Message('Account authorize',sender='13517078184@163.com',
#           recipients=['13517078184@139.com'])
# msg.body='邮件正文内容'




login_manager = LoginManager()
login_manager.init_app(app)  # flask-login模块初始化
Bootstrap(app)  # BootStrap支持
login_manager.login_view = "users.userlogin"
login_manager.session_protection = "strong"
# moment = Moment(app)  # 本地化时间支持
CORS(app)  # 跨域请求支持
mail.init_app(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(files_blueprint)

# with app.app_context():
#     mail.send(msg)



@login_manager.user_loader
def load_user(user_id):
    session = DBSession()
    user = session.query(User).filter(User.userid == user_id).first()
    session.close()
    return user

# @app.route('/files', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file:
#             filename = secure_filename(file.filename)
#             # print(os.path.join(os.getcwd(),'static', file.filename))
#             # file.save(os.path.join(os.getcwd(),'static',filename))
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return 'okk'
#     else:
#         return render_template('uploadtest.html')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('static',filename,as_attachment=True)


@app.route('/main',methods=['GET','POST'])
@app.route('/',methods=['GET','POST'])
@login_required
def main():
    return render_template('logout.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
