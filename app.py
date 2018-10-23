import os

from flask import Flask, request, render_template, flash, redirect,send_from_directory
from flask_login import LoginManager
from werkzeug.utils import secure_filename

from database import DBSession
from database import user as User
from users import users as user_blueprint


app = Flask(__name__)

app.secret_key = 'fsdfshfsdgfr346r93hrfwe8vh3bi4r7834rtn2cir5hv728'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static')


login_manager = LoginManager()
login_manager.init_app(app)  # flask-login模块初始化


app.register_blueprint(user_blueprint)

@login_manager.user_loader
def load_user(user_id):
    session = DBSession()
    user = session.query(User).filter(User.userid == user_id).first()
    session.close()
    return user

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            # print(os.path.join(os.getcwd(),'static', file.filename))
            # file.save(os.path.join(os.getcwd(),'static',filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'okk'
    else:
        return render_template('uploadtest.html')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('static',filename,as_attachment=True)


@app.route('/main',methods=['GET','POST'])
def main():
    return 'okk'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
