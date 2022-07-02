from flask import Flask
import pymongo

app = Flask(__name__)


@app.route('/')
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'harsaivmdbpro ucmbatc12749815'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    return app