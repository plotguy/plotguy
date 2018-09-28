from flask import Flask
from flask import render_template

application = Flask(__name__)

@application.route('/purchase')
def purchase():
    return render_template('purchase.html')

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()