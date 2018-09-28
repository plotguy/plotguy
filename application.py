from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os


UPLOAD_FOLDER = 'raw_uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['SECRET_KEY'] = 'naweeni'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            print(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            print('the filename is ' + filename)
            # return redirect(url_for('raw_uploads',
            #                         filename=filename))
            return 'success!'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input id="file" type="file" accept="image/*" name="file">
      <input type=submit value=Upload>
    </form>
    '''

@application.route('/purchase')
def purchase():
    return render_template('purchase.html')

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()