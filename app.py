import os

from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key='fsdfshfsdgfr346r93hrfwe8vh3bi4r7834rtn2cir5hv728'
ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif', 'docx')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        file=request.files['file']
        if file:
            file.save(os.path.join(os.getcwd(),'static'), file.filename)
        return 'okk'
    else:
        return render_template('uploadtest.html')


if __name__ == '__main__':
    app.run()
