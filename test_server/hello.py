from flask import Flask, render_template, url_for
app = Flask(__name__)

SERVER_NAME = "boxysean.com"
SERVER_PORT = 8080

@app.route("/")
def hello():
    return render_template('hello.html')

if app.config['DEBUG'] or True:
    from werkzeug import SharedDataMiddleware
    import os
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'static')
    })

if __name__ == "__main__":
    app.run(SERVER_NAME, SERVER_PORT)
