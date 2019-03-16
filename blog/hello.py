import redis
from flask import Flask
from flask_script import Manager
from flask_session import Session

from back.models import db
from back.views import back_blue
from web.views import web_blue

app = Flask(__name__)

app.register_blueprint(blueprint=back_blue)
app.register_blueprint(blueprint=web_blue, url_prefix='/web')

app.secret_key = 'qwe1asd2zxc3'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/user_admin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Session(app)
db.init_app(app)
manage = Manager(app)
if __name__ == '__main__':
    manage.run()
