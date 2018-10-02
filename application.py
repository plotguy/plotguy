from flask import Flask, render_template, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import boto3
import io


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
            # Do not hard code credentials
            client = boto3.client(
                's3',
                # TODO: get aws credentials configured on EBS
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY
            )
            bucket_name = 'plotguydatastore'
            client.upload_fileobj(file, bucket_name, file.filename)

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

@application.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        session['email'] = request.form['email']
        return redirect(url_for('draw'))
    return render_template('start.html')

@application.route('/draw', methods=['GET', 'POST'])
def draw():
    if request.method == 'POST':
        s3_client = boto3.client(
            's3',
            # TODO: get aws credentials configured on EBS
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY
        )
        bucket_name = 'plotguydatastore'
        svg_body = request.form['svg_data'].encode('utf-8')
        key = session['email'].split('@')[0] + '.svg'
        s3_client.put_object(Body=svg_body, Bucket=bucket_name, Key=key)

        db_client = boto3.client(
            'dynamodb',
            # TODO: get aws credentials configured on EBS
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name='us-west-1'
        )

        db_client.put_item(
            TableName="plotguy_v0",
            Item={
                'email': {'S': session['email']},
                'completed': {'N': '0'},
                'filepath': {'S': key},
            }
        )
        return render_template('success.html')

        #client.upload_fileobj(file, bucket_name, file.filename)
    return render_template('draw.html')


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()