from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/purchase')
def purchase():
    return render_template('purchase.html')

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()