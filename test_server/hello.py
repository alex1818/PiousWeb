from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
def hello():
    print "here"
    return render_template('hello.html')

if app.config['DEBUG'] or True:
    from werkzeug import SharedDataMiddleware
    import os
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'static')
    })

if __name__ == "__main__":
    app.run()
