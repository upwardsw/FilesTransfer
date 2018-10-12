import os

from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = 'fsdfshfsdgfr346r93hrfwe8vh3bi4r7834rtn2cir5hv728'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static')


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


if __name__ == '__main__':
    app.run()
